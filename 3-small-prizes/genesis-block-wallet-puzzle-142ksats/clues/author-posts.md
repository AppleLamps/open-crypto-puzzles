# Author posts, verbatim

Every message of this puzzle is an OP_RETURN output in a transaction that also pays the
escrow `bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj`. The author has no
other channel. The attribution below follows the transaction inputs: a message is the
author's when its inputs spend a change output of a previous author transaction (the
announcement is the anchor). Questions paid directly to an author change address were
re-posted by the author to the escrow before the answer; those re-posts are marked
"relayed". All times are UTC, read from the block timestamps on 2026-08-29.

## Announcement

2026-08-22 19:45:38, block 963,629, `b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77`, 5,000 sats to the escrow:

> I made a Bitcoin puzzle using information contained in the genesis block created by Satoshi to generate the wallet.
>
> The entropy is extremely low. I didn't even need to back anything up. Everything I needed was already in the genesis block.
>
> Good luck!

The escrow had been funded with 20,000 sats 17 hours earlier
(`e2aaa928a965ee02b9c9a76227383113a62f350701a18d7792372712ce501ac7`, block 963,517,
2026-08-22 02:45:22, no message).

## Hint channel

2026-08-23 01:51:20, block 963,659, `248f690de194372564baa14e1bebf08154e2f2042ed205baa6157fdc0e3f22ea`, 5,000 sats:

> If you have a question, you can include it with a transaction sent directly to this address, and I will reply with a hint.
>
> Larger payments receive better hints. Dust transactions will be ignored.

## Questions and answers

| Time | Block | Txid | From | To escrow | Text |
|---|---|---|---|---|---|
| 2026-08-23 14:41:38 | 963,739 | `3b2f8aef7bb8f56dc939b34465906fd8a7693b2c8718d541ea635f8780313db6` | player 1 | 12,916 sats | Is the witness script a hash lock, a multisig, or something else? |
| 2026-08-23 15:43:56 | 963,744 | `0fb7a2f175dd7f9b8826cf2923ce4fcb56e4c7bfe252903e6dad1f87f177dfe3` | author | 12,916 sats | The witness script is a multisig. |
| 2026-08-23 18:19:26 | 963,758 | `268093b9ae56a59d2bb1a6acde588d6763fe859947b098c235031493208d3e22` | author (relayed, player 1) | 16,028 sats | How many keys, what threshold, and how are the keys derived from genesis? |
| 2026-08-23 21:08:58 | 963,768 | `ef63243d374d8eabeac7e17e06cc4b1b672146dc61a8e5180eeac980cec07302` | author | 16,028 sats | Two keys, both required. The rest is for you to derive. |
| 2026-08-24 06:40:09 | 963,823 | `fe27df994d658e79bea7b4cfe2427341ce024c70c5af21b76186807eebe57072` | author (relayed, player 1) | 6,345 sats | Are both keys from the same genesis field, and is the function a hash? |
| 2026-08-24 07:13:18 | 963,829 | `82a076b02643372769ac676d260ef4d9854c6bf49370ed61875fc63b8241dcfc` | author | 2,000 sats | Yes, both keys use the same Genesis field, and there is no hash. |
| 2026-08-24 08:58:20 | 963,837 | `2f5bbc7c0d031f54c9b7c8bee73eb2607d04b19019d1deac7f773eafdd1b91f8` | author (relayed, player 1) | 12,843 sats | Is the second key derived from the first, or both from genesis independently? |
| 2026-08-24 14:32:47 | 963,868 | `ff884832e937f972c92c012ba235ff45b549cd1702dfd02691056da6bc1ff913` | author | 2,000 sats | Both keys are derived independently from Genesis. |
| 2026-08-24 18:01:41 | 963,888 | `69d19cc41b8a5f1e711d46069e301bb4d29223bfcf1128eb6a9236e0d3e9b96c` | player 1 | 12,703 sats | Which genesis field, hash, merkle, nonce, time, headline, or pubkey? |
| 2026-08-24 21:35:20 | 963,910 | `eb609dfede7f61d3bf9fe79ae48e546c358ebd09c05b3cd64a22433cb784ea86` | author | 2,000 sats | The Genesis Block is public. Which part of it matters is for you to discover. |
| 2026-08-28 17:38:24 | 964,465 | `51b9f9521ca5bfae851b0f55dc3b151914b95f77eef156078a422396cd30cef2` | player 2 | 2,000 sats | Prize Address?Genesis field 32 bytes or smaller? |
| 2026-08-28 20:15:31 | 964,477 | `84fc5defe22590a02bbe0025831be110ed6f9e0bc53c3c835a4e42479b0bf050` | player 2 | 3,000 sats | Give a hint at your will! |
| 2026-08-28 22:45:35 | 964,486 | `610fc4d2ca1a214d99248c8188fd2973f4c51fca319ccf9ab983ac3edf4b1821` | player 2 | 3,500 sats | Can you give any hint about derivation offset/rule? |
| 2026-08-28 23:15:28 | 964,491 | `6e94cfcbc1350a138242f97310dfd0280371a0020380cb32b2512337470c1077` | author | 5,000 sats | Solve it to find out. Maybe both. (newline) If you can't check the Genesis block, you can also use The Times newspaper! |
| 2026-08-28 23:50:52 | 964,496 | `8be479605bc8f2facd2036fd1b7f5cfa3a3f3920eeffee75e0004a2cff4d25d6` | author | 3,500 sats | `Derivation rule: root -> multisig -> mainnet -> genesis_data -> script_type` |

The three relayed questions were first paid by player 1 directly to the author's change
address of the moment, off the escrow's history: 32,357 sats on 2026-08-23 16:20:06
(`d271c37d8ce26247`), 6,465 sats on 2026-08-23 19:37:09 (`a2209eef7490846b`), 12,963 sats on
2026-08-24 03:35:54 (`f6579e67ff234ddb`). Player 1 also paid its first question twice, once
to the author (12,909 sats, `1b4bde84af7df419`, 14:34:56) and once to the escrow.
