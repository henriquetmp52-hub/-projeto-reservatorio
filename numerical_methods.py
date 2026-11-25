import numpy as np

def bisection(function, a, b, tolerance=1e-8, max_iterations=200):
    """Encontra uma raiz de function no intervalo [a,b] pelo método da bisseção."""
    fa = function(a)
    fb = function(b)
    if abs(fa) < tolerance:
        return a, 0
    if abs(fb) < tolerance:
        return b, 0
    if fa * fb > 0:
        raise ValueError(
            "A bisseção precisa de sinais opostos nas extremidades. "
            "O volume máximo disponível pode ser menor que o volume requerido."
        )
    for iteration in range(1, max_iterations + 1):
        midpoint = (a + b) / 2
        fm = function(midpoint)
        if abs(fm) < tolerance or (b - a) / 2 < tolerance:
            return midpoint, iteration
        if fa * fm < 0:
            b, fb = midpoint, fm
        else:
            a, fa = midpoint, fm
    return (a + b) / 2, max_iterations


def gaussian_elimination(A, b, tolerance=1e-12):
    """Resolve A x = b por eliminação de Gauss com pivotamento parcial."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A matriz A deve ser quadrada.")
    n = len(b)
    if A.shape != (n, n):
        raise ValueError("As dimensões de A e b não são compatíveis.")

    augmented = np.column_stack((A, b))
    for col in range(n):
        pivot_row = col + np.argmax(np.abs(augmented[col:, col]))
        if abs(augmented[pivot_row, col]) < tolerance:
            raise ValueError("Sistema singular ou sem solução única.")
        augmented[[col, pivot_row]] = augmented[[pivot_row, col]]
        for row in range(col + 1, n):
            factor = augmented[row, col] / augmented[col, col]
            augmented[row, col:] -= factor * augmented[col, col:]

    x = np.zeros(n)
    for row in range(n - 1, -1, -1):
        x[row] = (
            augmented[row, -1] -
            np.dot(augmented[row, row + 1:n], x[row + 1:n])
        ) / augmented[row, row]
    return x


def least_squares_line(x, y):
    """Ajusta y = a*x + b pelo método dos quadrados mínimos."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("Informe ao menos dois pares x,y.")
    design = np.column_stack((x, np.ones_like(x)))
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)
    return float(coefficients[0]), float(coefficients[1])
