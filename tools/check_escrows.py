#!/usr/bin/env python3
"""
check_escrows.py -- re-check every puzzle escrow against the chain.

Purpose:
    Read every puzzle folder manifest (or the generated puzzles.json when present), query
    the relevant chain for each address, and print a table of expected versus observed state.
    This is the tool "How to read this repository" step 3 points readers at: never trust a
    stale on-chain check date, re-run this.

Usage (run from the repository root):
    python3 tools/check_escrows.py                # every address in every manifest
    python3 tools/check_escrows.py --slug <slug>   # one puzzle only
    python3 tools/check_escrows.py --update        # also writes verified_on/verified_state
                                                    # back into the folder's puzzle.json

Input:
    puzzles.json if present at the repository root, otherwise every <tier>/<slug>/puzzle.json.

Output:
    One printed row per address: slug, label, address, expected, observed, spent, verdict.
    Exit code 1 if any address that a manifest claims is "funded-unspent" is observed as
    swept or unfunded. Network errors are printed as ERROR and never counted as a sweep.
"""

import argparse
import json
import os
import sys
from datetime import date

import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIERS = ["1-big-prizes", "2-mid-prizes", "3-small-prizes", "4-solved", "5-dead-ends"]

TIMEOUT = 15
RETRIES = 1  # one retry after the first attempt, so two attempts total

ETH_RPC_ENDPOINTS = ["https://eth.drpc.org", "https://cloudflare-eth.com"]
BASE_RPC_ENDPOINT = "https://mainnet.base.org"


def http_get(url, **kwargs):
    last_exc = None
    for attempt in range(RETRIES + 1):
        try:
            return requests.get(url, timeout=TIMEOUT, **kwargs)
        except requests.RequestException as exc:
            last_exc = exc
    raise last_exc


def http_post(url, json_body):
    last_exc = None
    for attempt in range(RETRIES + 1):
        try:
            return requests.post(url, json=json_body, timeout=TIMEOUT)
        except requests.RequestException as exc:
            last_exc = exc
    raise last_exc


def check_bitcoin(address):
    try:
        resp = http_get(f"https://mempool.space/api/address/{address}")
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return "ERROR", f"network error: {exc}"

    stats = data.get("chain_stats", {})
    funded = stats.get("funded_txo_sum", 0)
    spent = stats.get("spent_txo_sum", 0)
    if funded == 0:
        return "unfunded", f"funded={funded} spent={spent}"
    if spent == 0:
        return "funded-unspent", f"funded={funded} spent={spent}"
    if spent >= funded:
        return "swept", f"funded={funded} spent={spent}"
    return "partially-spent", f"funded={funded} spent={spent}"


def _eth_rpc(url, method, params):
    resp = http_post(url, {"jsonrpc": "2.0", "method": method, "params": params, "id": 1})
    resp.raise_for_status()
    body = resp.json()
    if "error" in body:
        raise RuntimeError(body["error"])
    return body["result"]


def check_evm(address, endpoints):
    last_exc = None
    for url in endpoints:
        try:
            balance_hex = _eth_rpc(url, "eth_getBalance", [address, "latest"])
            tx_count_hex = _eth_rpc(url, "eth_getTransactionCount", [address, "latest"])
            balance_wei = int(balance_hex, 16)
            tx_count = int(tx_count_hex, 16)
            if balance_wei == 0 and tx_count == 0:
                return "unfunded", f"balance=0 nonce=0 (via {url})"
            if balance_wei == 0 and tx_count > 0:
                return "swept", f"balance=0 nonce={tx_count} (via {url})"
            return "funded-unspent", f"balance_wei={balance_wei} nonce={tx_count} (via {url})"
        except Exception as exc:
            last_exc = exc
            continue
    return "ERROR", f"network error: {last_exc}"


def check_ethereum(address):
    return check_evm(address, ETH_RPC_ENDPOINTS)


def check_base(address):
    return check_evm(address, [BASE_RPC_ENDPOINT])


def check_arweave(address):
    try:
        resp = http_get(f"https://arweave.net/wallet/{address}/balance")
        resp.raise_for_status()
        winston = int(resp.text.strip())
    except Exception as exc:
        return "ERROR", f"network error: {exc}"
    ar = winston / 1e12
    if winston == 0:
        return "unfunded", f"balance={ar} AR"
    return "funded-unspent", f"balance={ar} AR"


def check_address(entry):
    chain = entry.get("chain", "")
    address = entry.get("address", "")
    if chain == "bitcoin":
        return check_bitcoin(address)
    if chain == "ethereum":
        return check_ethereum(address)
    if chain == "base":
        return check_base(address)
    if chain == "arweave":
        return check_arweave(address)
    if chain == "solana":
        return "SKIPPED", "Solana is not queried automatically; check https://solscan.io/account/<address> by hand."
    return "ERROR", f"unknown chain: {chain}"


def load_puzzles(slug_filter=None):
    puzzles_json_path = os.path.join(REPO_ROOT, "puzzles.json")
    puzzles = []
    if os.path.isfile(puzzles_json_path):
        with open(puzzles_json_path, encoding="utf-8") as f:
            doc = json.load(f)
        puzzles = doc.get("puzzles", [])
    else:
        for tier_dir_name in TIERS:
            tier_dir = os.path.join(REPO_ROOT, tier_dir_name)
            if not os.path.isdir(tier_dir):
                continue
            for entry in sorted(os.listdir(tier_dir)):
                manifest_path = os.path.join(tier_dir, entry, "puzzle.json")
                if os.path.isfile(manifest_path):
                    with open(manifest_path, encoding="utf-8") as f:
                        manifest = json.load(f)
                    manifest["folder"] = f"{tier_dir_name}/{entry}"
                    puzzles.append(manifest)

    if slug_filter:
        puzzles = [p for p in puzzles if p.get("slug") == slug_filter]
    return puzzles


def update_manifest(puzzle, results_by_address):
    folder = puzzle.get("folder")
    if not folder:
        print(f"  (skip --update: {puzzle.get('slug')} has no folder, it is a row-only entry)")
        return
    manifest_path = os.path.join(REPO_ROOT, folder, "puzzle.json")
    if not os.path.isfile(manifest_path):
        print(f"  (skip --update: {manifest_path} not found)")
        return
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    today = date.today().isoformat()
    changed = False
    for addr_entry in manifest.get("addresses", []):
        address = addr_entry.get("address")
        if address in results_by_address:
            state, _detail = results_by_address[address]
            if state != "ERROR" and state != "SKIPPED":
                addr_entry["verified_on"] = today
                addr_entry["verified_state"] = state
                changed = True
    if changed:
        manifest["last_updated"] = today
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"  updated {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description="Re-check puzzle escrows against the chain.")
    parser.add_argument("--slug", default=None, help="only check this puzzle slug")
    parser.add_argument("--update", action="store_true", help="write verified_on/verified_state back into the folder manifest")
    args = parser.parse_args()

    puzzles = load_puzzles(args.slug)
    if not puzzles:
        print("No puzzles found (0 manifests). Nothing to check.")
        sys.exit(0)

    header = f"{'slug':<45} {'label':<10} {'address':<44} {'expected':<20} {'observed':<16} {'verdict'}"
    print(header)
    print("-" * len(header))

    any_drift = False

    for puzzle in puzzles:
        slug = puzzle.get("slug", "")
        addresses = puzzle.get("addresses", [])
        results_by_address = {}
        for addr_entry in addresses:
            address = addr_entry.get("address", "")
            label = addr_entry.get("label", "")
            expected = addr_entry.get("expected", "")
            claimed_state = addr_entry.get("verified_state", "unknown")

            state, detail = check_address(addr_entry)
            results_by_address[address] = (state, detail)

            verdict = "OK"
            if state == "ERROR":
                verdict = "ERROR (network, not a verdict)"
            elif state == "SKIPPED":
                verdict = "SKIPPED"
            elif claimed_state == "funded-unspent" and state in ("swept", "unfunded"):
                verdict = f"DRIFT: manifest says funded-unspent, chain says {state}"
                any_drift = True
            elif claimed_state != state:
                verdict = f"NOTE: manifest says {claimed_state}, chain says {state}"

            print(f"{slug:<45} {label:<10} {address:<44} {expected:<20} {state:<16} {verdict}")
            if detail:
                print(f"  detail: {detail}")

        if args.update and addresses:
            update_manifest(puzzle, results_by_address)

    if any_drift:
        print("\nAt least one address that a manifest claims is funded-unspent is now swept or unfunded.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
