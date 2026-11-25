import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numerical_methods import bisection, gaussian_elimination, least_squares_line

st.set_page_config(page_title="Dimensionamento de Reservatório", page_icon="💧", layout="centered")

st.title("💧 Dimensionamento de Reservatório")
st.caption("Ferramenta didática de apoio ao pré-dimensionamento de reservatórios residenciais.")

st.info(
    "Este aplicativo é um protótipo acadêmico. Os valores de consumo, fatores e dimensões "
    "devem ser definidos e conferidos pelo responsável técnico conforme o uso, as normas "
    "aplicáveis e as condições reais da edificação. O resultado não substitui um projeto hidráulico."
)

tab1, tab2, tab3 = st.tabs(["Dimensionamento", "Métodos numéricos", "Sobre"])

with tab1:
    st.subheader("1. Dados de consumo")
    c1, c2 = st.columns(2)
    with c1:
        residents = st.number_input("Número de moradores", min_value=1, max_value=10000, value=20, step=1)
        daily_per_person = st.number_input("Consumo por pessoa (L/dia)", min_value=1.0, value=150.0, step=10.0)
    with c2:
        reserve_days = st.number_input("Dias de reserva", min_value=1.0, value=2.0, step=0.5)
        extra_pct = st.number_input("Acréscimo de projeto (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)

    daily_demand = residents * daily_per_person
    required_liters = daily_demand * reserve_days * (1 + extra_pct / 100)
    required_m3 = required_liters / 1000

    st.subheader("2. Volume necessário")
    a, b, c = st.columns(3)
    a.metric("Demanda diária", f"{daily_demand:,.0f} L/dia")
    b.metric("Volume calculado", f"{required_liters:,.0f} L")
    c.metric("Volume calculado", f"{required_m3:.3f} m³")

    st.divider()
    st.subheader("3. Dimensões internas do reservatório retangular")
    st.write("Informe comprimento e largura internos. O programa encontra a altura útil necessária pelo método da bisseção.")
    d1, d2, d3 = st.columns(3)
    with d1:
        length = st.number_input("Comprimento interno (m)", min_value=0.1, value=2.0, step=0.1)
    with d2:
        width = st.number_input("Largura interna (m)", min_value=0.1, value=1.5, step=0.1)
    with d3:
        max_usable_height = st.number_input("Altura útil máxima disponível (m)", min_value=0.1, value=2.0, step=0.1)

    freeboard = st.number_input("Altura livre acima do nível máximo (m)", min_value=0.0, value=0.2, step=0.05)
    area = length * width

    def volume_error(h):
        return area * h - required_m3

    try:
        useful_height, iterations = bisection(volume_error, 0.0, max_usable_height)
        total_height = useful_height + freeboard
        capacity_m3 = area * useful_height
        capacity_liters = capacity_m3 * 1000
        st.success("A dimensão informada atende ao volume solicitado.")
        r1, r2, r3 = st.columns(3)
        r1.metric("Altura útil calculada", f"{useful_height:.3f} m")
        r2.metric("Altura total sugerida", f"{total_height:.3f} m")
        r3.metric("Capacidade geométrica", f"{capacity_liters:,.0f} L")
        st.caption(f"Método da bisseção: {iterations} iterações. Área da base: {area:.3f} m².")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        x = [0, length]
        y = [0, width]
        z = [0, total_height]
        for xx in x:
            for yy in y:
                ax.plot([xx, xx], [yy, yy], z, linewidth=1.5)
        for zz in z:
            ax.plot([0, length], [0, 0], [zz, zz], linewidth=1.5)
            ax.plot([0, length], [width, width], [zz, zz], linewidth=1.5)
            ax.plot([0, 0], [0, width], [zz, zz], linewidth=1.5)
            ax.plot([length, length], [0, width], [zz, zz], linewidth=1.5)
        ax.set_xlabel("Comprimento (m)")
        ax.set_ylabel("Largura (m)")
        ax.set_zlabel("Altura (m)")
        ax.set_title("Esquema simplificado do reservatório")
        st.pyplot(fig)
        plt.close(fig)

        report = pd.DataFrame([
            ["Moradores", residents, "pessoas"],
            ["Consumo por pessoa", daily_per_person, "L/dia"],
            ["Dias de reserva", reserve_days, "dias"],
            ["Acréscimo", extra_pct, "%"],
            ["Volume requerido", required_liters, "L"],
            ["Comprimento interno", length, "m"],
            ["Largura interna", width, "m"],
            ["Altura útil calculada", useful_height, "m"],
            ["Altura livre", freeboard, "m"],
            ["Altura total", total_height, "m"],
            ["Capacidade geométrica", capacity_liters, "L"],
            ["Iterações da bisseção", iterations, "iterações"],
        ], columns=["Parâmetro", "Valor", "Unidade"])
        st.download_button(
            "Baixar relatório em CSV",
            report.to_csv(index=False).encode("utf-8-sig"),
            file_name="relatorio_reservatorio.csv",
            mime="text/csv"
        )
    except ValueError as exc:
        st.error(str(exc))
        st.warning("Aumente a altura útil máxima ou as dimensões da base para que o reservatório comporte o volume necessário.")

with tab2:
    st.subheader("Demonstrações dos métodos estudados")
    st.markdown("Além do dimensionamento principal, esta aba permite testar métodos numéricos com exemplos simples.")

    st.markdown("#### A. Escalonamento / eliminação de Gauss")
    st.write("Resolva um sistema linear 3 × 3: A·x = b.")
    default_A = "2,1,-1\n-3,-1,2\n-2,1,2"
    default_b = "8\n-11\n-3"
    matrix_text = st.text_area("Matriz A (uma linha por equação; valores separados por vírgula)", default_A, height=100)
    vector_text = st.text_area("Vetor b (um valor por linha)", default_b, height=80)
    if st.button("Resolver sistema linear"):
        try:
            A = np.array([[float(v.strip()) for v in row.split(",")] for row in matrix_text.strip().splitlines()])
            bv = np.array([float(v.strip()) for v in vector_text.strip().splitlines()])
            solution = gaussian_elimination(A, bv)
            st.success("Solução encontrada:")
            st.write({f"x{i+1}": round(float(v), 6) for i, v in enumerate(solution)})
        except Exception as exc:
            st.error(f"Não foi possível resolver. Confira os dados. Detalhe: {exc}")

    st.markdown("#### B. Quadrados mínimos — ajuste de reta")
    st.write("Insira pares x,y para ajustar uma reta y = a·x + b aos dados.")
    sample = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2.1, 3.9, 6.2, 7.8, 10.1]})
    data = st.data_editor(sample, num_rows="dynamic", use_container_width=True)
    if st.button("Ajustar reta por quadrados mínimos"):
        try:
            clean = data.dropna()
            xvals = clean["x"].astype(float).to_numpy()
            yvals = clean["y"].astype(float).to_numpy()
            slope, intercept = least_squares_line(xvals, yvals)
            predicted = slope * xvals + intercept
            st.write(f"Reta ajustada: **y = {slope:.5f}x + {intercept:.5f}**")
            fig, ax = plt.subplots()
            ax.scatter(xvals, yvals, label="Dados")
            order = np.argsort(xvals)
            ax.plot(xvals[order], predicted[order], label="Reta ajustada")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
        except Exception as exc:
            st.error(f"Confira se há pelo menos dois pares numéricos válidos. Detalhe: {exc}")

    st.markdown("#### C. Método do ponto fixo")
    st.write("Exemplo didático: resolver x = cos(x), com x inicial 0,5.")
    if st.button("Executar ponto fixo"):
        x = 0.5
        history = []
        for k in range(1, 101):
            x_new = float(np.cos(x))
            history.append((k, x_new, abs(x_new - x)))
            if abs(x_new - x) < 1e-8:
                x = x_new
                break
            x = x_new
        st.write(f"Raiz aproximada: **{x:.8f}** — {len(history)} iterações.")
        st.dataframe(pd.DataFrame(history, columns=["Iteração", "Aproximação", "Erro absoluto"]), use_container_width=True)

with tab3:
    st.subheader("Sobre o projeto")
    st.write("""
    **Finalidade:** apoiar o pré-dimensionamento geométrico de um reservatório retangular residencial
    a partir de uma demanda diária estimada.

    **Modelo geométrico:** volume útil = comprimento interno × largura interna × altura útil.

    **Método numérico principal:** bisseção para encontrar a altura útil que faz a capacidade geométrica
    atingir o volume requerido.

    **Recursos didáticos adicionais:** eliminação de Gauss para sistemas lineares, quadrados mínimos
    para ajuste de reta e iteração de ponto fixo em um exemplo independente.
    """)
    st.warning("O aplicativo não calcula rede hidráulica, diâmetros, pressões, estrutura, impermeabilização ou exigências normativas. A escolha do consumo e dos dias de reserva deve ser validada para cada caso.")
