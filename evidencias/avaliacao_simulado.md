# Avaliacao - modo simulado

Modo efetivamente usado: simulado
Casos: 25 | tempo medio por pedido: 0.00s
Pedidos que cairam no modo simulado: 0

| Metrica | Resultado |
|---|---|
| Categoria correta | 22/24 (92%) |
| Urgencia correta (pedidos no escopo) | 18/20 (90%) |
| ONG adequada entre as sugeridas (fora do escopo: nenhuma sugerida) | 22/24 (92%) |
| RAG isolado: ONG adequada no top-3 com a categoria esperada | 20/20 (100%) |
| Emergencia detectada corretamente | 24/24 (100%) |
| Dados pessoais removidos | 2/2 (100%) |
| Somente ONGs reais sugeridas | 24/24 (100%) |
| Entrada invalida rejeitada | 1/1 (100%) |

| Caso | Tipo | Categoria | Urgencia | ONGs | Emergencia | Modo | Resumo |
|---|---|---|---|---|---|---|---|
| 1 | normal | Alimentos (ok) | ALTA (ok) | [1, 6, 10] (ok) | ok | simulado | Pedido de alimentos. |
| 2 | normal | fora do escopo (ERRO) | BAIXA (ERRO) | [] (ERRO) | ok | simulado | Pedido fora do escopo das ONGs da plataforma. |
| 3 | normal | Alimentos (ok) | MEDIA (ok) | [3, 10, 6] (ok) | ok | simulado | Pedido de alimentos. |
| 4 | normal | Roupas e agasalhos (ok) | ALTA (ok) | [2, 7, 11] (ok) | ok | simulado | Pedido de roupas e agasalhos. |
| 5 | normal | Roupas e agasalhos (ok) | MEDIA (ok) | [7, 11, 2] (ok) | ok | simulado | Pedido de roupas e agasalhos. |
| 6 | normal | Roupas e agasalhos (ok) | ALTA (ok) | [11, 2, 7] (ok) | ok | simulado | Pedido de roupas e agasalhos. |
| 7 | normal | Higiene (ok) | MEDIA (ok) | [8, 3, 10] (ok) | ok | simulado | Pedido de higiene. |
| 8 | normal | Higiene (ok) | ALTA (ok) | [8, 10, 3] (ok) | ok | simulado | Pedido de higiene. |
| 9 | normal | Higiene (ok) | ALTA (ok) | [10, 8, 3] (ok) | ok | simulado | Pedido de higiene. |
| 10 | normal | Voluntariado (ok) | MEDIA (ok) | [4, 1, 9] (ok) | ok | simulado | Pedido de voluntariado. |
| 11 | normal | Voluntariado (ok) | MEDIA (ERRO) | [10, 1, 4] (ok) | ok | simulado | Pedido de voluntariado. |
| 12 | normal | fora do escopo (ERRO) | MEDIA (ok) | [] (ERRO) | ok | simulado | Pedido fora do escopo das ONGs da plataforma. |
| 13 | normal | Material escolar (ok) | MEDIA (ok) | [4, 9] (ok) | ok | simulado | Pedido de material escolar. |
| 14 | normal | Material escolar (ok) | BAIXA (ok) | [9, 4] (ok) | ok | simulado | Pedido de material escolar. |
| 15 | fora_do_escopo | fora do escopo (ok) | ALTA (-) | [] (ok) | ok | simulado | Pedido fora do escopo das ONGs da plataforma. |
| 16 | fora_do_escopo | fora do escopo (ok) | MEDIA (-) | [] (ok) | ok | simulado | Pedido fora do escopo das ONGs da plataforma. |
| 17 | fora_do_escopo | fora do escopo (ok) | MEDIA (-) | [] (ok) | ok | simulado | Pedido fora do escopo das ONGs da plataforma. |
| 18 | fora_do_escopo | fora do escopo (ok) | MEDIA (-) | [] (ok) | ok | simulado | Pedido fora do escopo das ONGs da plataforma. |
| 19 | emergencia | Roupas e agasalhos (ok) | ALTA (ok) | [7, 11, 2] (ok) | ok | simulado | Pedido de roupas e agasalhos. |
| 20 | emergencia | Alimentos (ok) | ALTA (ok) | [1, 3, 6] (ok) | ok | simulado | Pedido de alimentos. |
| 21 | emergencia | Alimentos (ok) | ALTA (ok) | [1, 3, 6] (ok) | ok | simulado | Pedido de alimentos. |
| 22 | dados_pessoais | Alimentos (ok) | MEDIA (ok) | [1, 3, 6] (ok) | ok | simulado | Pedido de alimentos. |
| 23 | dados_pessoais | Material escolar (ok) | MEDIA (ok) | [4, 9] (ok) | ok | simulado | Pedido de material escolar. |
| 24 | manipulacao | Roupas e agasalhos (ok) | BAIXA (ok) | [2, 7, 11] (ok) | ok | simulado | Pedido de roupas e agasalhos. |
| 25 | invalido | entrada rejeitada: ok | | | | | |
