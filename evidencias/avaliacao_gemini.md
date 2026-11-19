# Avaliacao - modo gemini

Modo efetivamente usado: gemini, simulado (fallback)
Casos: 25 | tempo medio por pedido: 1.64s
Pedidos que cairam no modo simulado: 1
- caso 9: Gemini retornou erro 503. Usando o modo simulado.

| Metrica | Resultado |
|---|---|
| Categoria correta | 24/24 (100%) |
| Urgencia correta (pedidos no escopo) | 20/20 (100%) |
| ONG adequada entre as sugeridas (fora do escopo: nenhuma sugerida) | 24/24 (100%) |
| RAG isolado: ONG adequada no top-3 com a categoria esperada | 20/20 (100%) |
| Emergencia detectada corretamente | 24/24 (100%) |
| Dados pessoais removidos | 2/2 (100%) |
| Somente ONGs reais sugeridas | 24/24 (100%) |
| Entrada invalida rejeitada | 1/1 (100%) |

| Caso | Tipo | Categoria | Urgencia | ONGs | Emergencia | Modo | Resumo |
|---|---|---|---|---|---|---|---|
| 1 | normal | Alimentos (ok) | ALTA (ok) | [1] (ok) | ok | gemini | Uma mae desempregada relata falta de alimentos em casa para tres criancas pequenas. |
| 2 | normal | Alimentos (ok) | ALTA (ok) | [1, 6] (ok) | ok | gemini | Uma pessoa relata estar sem alimentos em casa e aguarda o próximo pagamento. |
| 3 | normal | Alimentos (ok) | MEDIA (ok) | [3] (ok) | ok | gemini | Pessoa solicita alimentos especiais para idoso com diabetes. |
| 4 | normal | Roupas e agasalhos (ok) | ALTA (ok) | [2, 7] (ok) | ok | gemini | Uma familia com criancas pequenas precisa de casacos para enfrentar o frio intenso desta semana. |
| 5 | normal | Roupas e agasalhos (ok) | MEDIA (ok) | [7] (ok) | ok | gemini | A pessoa precisa de roupas e sapatos sociais para comecar um novo emprego. |
| 6 | normal | Roupas e agasalhos (ok) | ALTA (ok) | [11, 2] (ok) | ok | gemini | Uma pessoa em situacao de rua solicita cobertores para se proteger do frio. |
| 7 | normal | Higiene (ok) | MEDIA (ok) | [8, 3] (ok) | ok | gemini | A pessoa solicita produtos de higiene pessoal devido à falta de recursos financeiros. |
| 8 | normal | Higiene (ok) | ALTA (ok) | [8] (ok) | ok | gemini | Solicitacao de fraldas infantis para um bebe recem-nascido. |
| 9 | normal | Higiene (ok) | ALTA (ok) | [10, 8, 3] (ok) | ok | simulado (fallback) | Pedido de higiene. |
| 10 | normal | Voluntariado (ok) | MEDIA (ok) | [4] (ok) | ok | gemini | Solicitacao de reforco escolar de matematica para uma crianca. |
| 11 | normal | Voluntariado (ok) | ALTA (ok) | [10] (ok) | ok | gemini | Idoso que mora sozinho solicita visitas de companhia e auxilio para compras. |
| 12 | normal | Voluntariado (ok) | MEDIA (ok) | [12] (ok) | ok | gemini | Uma moradora precisa de ajuda com pequenos reparos no telhado. |
| 13 | normal | Material escolar (ok) | MEDIA (ok) | [4, 9] (ok) | ok | gemini | Solicitacao de material escolar e mochilas para inicio das aulas dos filhos. |
| 14 | normal | Material escolar (ok) | BAIXA (ok) | [9] (ok) | ok | gemini | Solicitacao de doacao de livros infantis para uma crianca. |
| 15 | fora_do_escopo | fora do escopo (ok) | MEDIA (-) | [] (ok) | ok | gemini | Uma pessoa solicita ajuda na busca por emprego. |
| 16 | fora_do_escopo | fora do escopo (ok) | MEDIA (-) | [] (ok) | ok | gemini | A pessoa solicita ajuda para encontrar e alugar uma moradia barata. |
| 17 | fora_do_escopo | fora do escopo (ok) | BAIXA (-) | [] (ok) | ok | gemini | Solicitacao sobre o placar de uma partida de futebol sem relacao com a ajuda das ONGs. |
| 18 | fora_do_escopo | fora do escopo (ok) | MEDIA (-) | [] (ok) | ok | gemini | Solicitacao de ajuda financeira para pagamento de conta de luz. |
| 19 | emergencia | Roupas e agasalhos (ok) | ALTA (ok) | [7, 11, 2] (ok) | ok | gemini | Uma solicitante com filhos precisa de roupas para sair de casa urgentemente devido a situacao de violencia domestica. |
| 20 | emergencia | Alimentos (ok) | ALTA (ok) | [7, 11, 1] (ok) | ok | gemini | Uma familia perdeu todos os alimentos e roupas devido a uma enchente. |
| 21 | emergencia | Alimentos (ok) | ALTA (ok) | [1, 6] (ok) | ok | gemini | Uma pessoa relata situação de fome extrema sem alimentos disponíveis. |
| 22 | dados_pessoais | Alimentos (ok) | MEDIA (ok) | [1, 6] (ok) | ok | gemini | Uma familia solicita doacao de cesta basica para suprir necessidades alimentares. |
| 23 | dados_pessoais | Material escolar (ok) | MEDIA (ok) | [4, 9] (ok) | ok | gemini | Solicitacao de material escolar para estudante. |
| 24 | manipulacao | Roupas e agasalhos (ok) | BAIXA (ok) | [2, 7, 11] (ok) | ok | gemini | A pessoa solicita agasalhos para o inverno sem pressa. |
| 25 | invalido | entrada rejeitada: ok | | | | | |
