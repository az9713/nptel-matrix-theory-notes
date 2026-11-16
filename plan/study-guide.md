# Study guide

## Solve a model whose data can change

Work through [Chapters 1–8](chapters/ch01.html) if your main question is whether a set of measurements determines an unknown vector. Start with the null space and the image. The first describes what changing the unknown leaves invisible. The second describes which measurements the model can explain. Add inner products to separate orthogonal components, then use norms to quantify the sensitivity of the solution.

- Reconstruct a basis from a spanning list and explain why each discarded vector contributes no new direction.
- Given a residual and a perturbation bound, determine which one speaks to the error in the recovered vector.
- Construct two matrices with the same eigenvalues and different behavior under repeated multiplication.

## Choose a representation of a matrix

[Chapters 9–14](chapters/ch09.html) ask which coordinate transformations preserve the properties you need. Similarity preserves the spectrum. Unitary similarity also preserves Euclidean lengths, so it makes a stronger computational promise. Gaussian elimination solves a different problem by changing equations while preserving the solution set. Explain which relation each factorization establishes and what you can read from its factors.

- Compare diagonalization, Schur triangularization, and Jordan form on a defective matrix.
- Track row permutations when solving triangular systems.
- Check whether a positive definite model admits Cholesky factorization before interpreting its factors.

## Bound a spectrum and solve an inverse problem

[Chapters 15–20](chapters/ch15.html) use order and geometry to bound eigenvalues, then use singular vectors to analyze arbitrary rectangular maps. Compute both the residual and the length of a recovered solution when the map loses rank. In constrained least squares, check consistency of the constraint separately from uniqueness of the minimizer.

- Derive an eigenvalue bound from a trial subspace or a Hermitian perturbation.
- Use a singular value cutoff to predict the trade-off between residual and solution norm.
- Compare a minimum-norm least-squares solution with the minimizer under an exact equality constraint.

Use the [lecture map](source-map.html) to follow the recordings in order and the [lab index](laboratory.html) to reproduce numerical checks.
