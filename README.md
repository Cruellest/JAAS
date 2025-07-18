# Jinja As An Service

Proof of concept, using jinja as an external service decoupled from any code to generate docx documents.

> Demo: https://jaas.cruellest.net

#### How to use:

##### Generate document based on docx template

```
# 1. A ferramenta e o método
curl -X 'POST' \

# 2. O endereço de destino (o endpoint da sua API)
  'http://127.0.0.1:8000/gerar-documento/' \

# 3. Instruções/Cabeçalhos (Headers) para o servidor
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \

# 4. O conteúdo do formulário (a "encomenda")
  -F 'template_file=@template.docx' \
  -F 'context_json={...}' \

# 5. O que fazer com a resposta do servidor
  --output documento_gerado.docx
```