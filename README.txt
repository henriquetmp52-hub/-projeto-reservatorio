# Projeto: Dimensionamento de Reservatório

## Requisitos
- Windows 10 ou 11
- Python 3.10 ou superior
- Conexão com a internet na primeira instalação das bibliotecas

## Instalação (uma única vez)
1. Instale o Python em https://www.python.org/downloads/
2. Durante a instalação, marque **Add Python to PATH**.
3. Abra a pasta deste projeto no VS Code.
4. Abra o terminal do VS Code (Terminal > New Terminal).
5. Execute:

```bash
python -m pip install -r requirements.txt
```

## Como executar
No terminal, dentro da pasta do projeto, execute:

```bash
python -m streamlit run main.py
```

O navegador abrirá a interface. Se não abrir automaticamente, copie o endereço local exibido no terminal (normalmente http://localhost:8501).

## O que o programa faz
- Calcula a demanda e o volume de reserva a partir dos dados informados.
- Calcula a altura útil necessária para uma base retangular informada.
- Usa o método da bisseção para encontrar essa altura.
- Desenha um esquema 3D simplificado e permite baixar um relatório CSV.
- Inclui demonstrações de eliminação de Gauss, quadrados mínimos e ponto fixo.

## Exemplo para testar
- Moradores: 20
- Consumo: 150 L/pessoa/dia
- Dias de reserva: 2
- Acréscimo: 0%
- Comprimento interno: 2 m
- Largura interna: 1,5 m
- Altura útil máxima: 2 m
- Altura livre: 0,2 m

Resultado esperado: volume requerido = 6.000 L; área da base = 3 m²; altura útil calculada = 2 m.

## Observações técnicas importantes
Este é um protótipo acadêmico de pré-dimensionamento, não um projeto executivo. O consumo diário, os dias de reserva, os fatores adotados e as dimensões devem ser definidos conforme o tipo de ocupação, exigências locais, normas aplicáveis e orientação do professor/profissional responsável. A altura livre é somada à altura útil e não entra no volume útil calculado. O programa não verifica estrutura, fundação, impermeabilização, tampa, acesso, tubulações, pressões ou requisitos sanitários.
