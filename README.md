# gps-bot

Bot para gerar guias GPS do INSS de forma automatizada.

Presente no site [SAL - Sistema de Acréscimos Legais](http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml) para contribuintes filiados a partir de 29/11/1999.

## Comportamento

Esse bot funciona com as seguintes três categorias:

- Contribuinte Individual
- Facultativo
- Segurado Especial

O pagamento do valor da guia é baseado sempre no teto do INSS (esse valor é descoberto de forma automática pelo bot), caso deseje mudar esse valor algumas partes do código devem ser alteradas.

O pagamento é sempre referente ao primeiro mês no qual o boleto ainda não venceu (o último dia de pagamento é sempre no dia 15 do mês seguinte). Por exemplo, caso o bot seja executado do dia 16/06 ao dia 15/07, o boleto gerado será referente ao mês 06. O dia de vencimento de todo boleto é sempre o dia útil mais próximo do dia 15.

Após geração do boleto pelo bot, um email é enviado para algum email desejado utilizando a [Gmail API](https://developers.google.com/gmail/api/guides/sending). Esse email contém o boleto no formato HTML como anexo e o código de barras bem como a categoria selecionada no corpo do email caso ele tenha sido executado com sucesso. Caso algum erro tenha ocorrido, um email também é enviado ao usuário informando que algum erro ocorreu durante a execução do programa.

## Observações técnicas

O site requer que o usuário resolva um CAPTCHA, por conta disso, é utilizado aqui o serviço [2Captcha](https://2captcha.com/) que é especializado em resolver esse tipo de verificação.

O bot prevê o deploy no site [Heroku](https://www.heroku.com/) então é altamente recomendado o seu uso. Além disso, o código foi feito para ser executado periodicamente (uma vez por dia) usando o [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler).

Para passar da tela em que o CAPTCHA é verificado, é utilizado o módulo [Selenium](https://selenium-python.readthedocs.io/) do python. Os outros passos são realizados através de requisições.

## Passos para o deploy no Heroku

- Crie uma conta em [2Captcha](https://2captcha.com/) e copie a `API_KEY` gerada no site.

- Edite o arquivo `constants_example.py`, preenchendo os dados em branco e o renomeie para `constants.py`.

- Para que a Gmail API funcione, siga os passos presentes no seguinte tutorial: https://www.thepythoncode.com/article/use-gmail-api-in-python. Coloque os arquivos necessários para autenticação na pasta `auth`.

- Siga os passos presentes na [documentação do Heroku](https://devcenter.heroku.com/articles/git) para fazer o deploy.

- Adicione o add-on [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler) ao app com frequência diária (ele irá rodar nos dias presentes no vetor `DAYS_TO_WORK` no arquivo `constants.py`). Coloque o comando `python -c 'import sys; sys.path.append("./src"); import main; main.execute()'` para ser executado.
