# inss-gps-bot

🇧🇷 

Bot para gerar guias GPS do INSS de forma automatizada. Utiliza Rest API e Web Scraping.

Presente no site [SAL - Sistema de Acréscimos Legais](http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml) para contribuintes filiados a partir de 29/11/1999.

Você pode ver o flow realizado toda vez que o bot é executado no vídeo abaixo.

🇬🇧 

Generate payment instructions (GPS) the from Brazilian Social Welfare (INSS) in an automated way. It uses Rest API and Web Scraping.

Present in the website [SAL - Sistema de Acréscimos Legais](http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml) to taxpayers enrolled from 29/11/1999.

You can see the flow performed every time the bot runs in the video below.

https://user-images.githubusercontent.com/26277944/179625950-ba78c74a-a2c3-4462-adf2-ea8df3231f47.mp4

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

- Edite o arquivo `src/constants_example.py`, preenchendo os dados em branco e o renomeie para `src/constants.py`.

- Para que a Gmail API funcione, siga os passos presentes no seguinte tutorial: https://www.thepythoncode.com/article/use-gmail-api-in-python. Coloque os arquivos necessários para autenticação na pasta `src/auth`.

- Siga os passos presentes na [documentação do Heroku](https://devcenter.heroku.com/articles/git) para fazer o deploy.

- Adicione o add-on [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler) ao app. Caso deseje rodar o bot com frequência diária, mas só o executar de fato em alguns dias do mês, coloque o comando `python -c 'import sys; sys.path.append("./src"); import main; main.execute_day_restriction([10, 28])''` para ser executado. No exemplo anterior, ele executaria o bot nos dias 10 e 28 de cada mês do ano.
