# FAQ

**Does this render a finished commercial by itself?**
No. The quickstart proves previs, the edit, and QA on synthetic media. A real spot still needs your footage or a model account you control.

**Which model does it require?**
None. MiniMax and Seedance are examples of official APIs. Another vendor belongs behind the same four methods.

**Will it upload my key anywhere except that vendor?**
The bundled adapters send the key only to the host in `MINIMAX_API_BASE` or `ARK_API_BASE`. There is no project account.

**Can my company use it for client work?**
Yes. Client work, hosted, SaaS, or multi-tenant services, and selling the software are permitted under the terms of Apache License 2.0. See [LICENSE](../LICENSE).

**Can I sell the videos?**
Yes. Outputs belong to you, subject to your inputs and to the model vendor's terms.

**Why is face detection off?**
The `buffalo_s` weights and the SyncNet weights are research-licensed. Turn them on only when your use is allowed. See [model weights](model-weights.md).

**Blender is large. Do I need it?**
No. `--backend raster` is the default of the quickstart and needs `numpy` and `Pillow`.

**Where do the demo films go?**
See [demos](demos/README.md). Leave the TODO lines in place until a file we have rights to is ready.
