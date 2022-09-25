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

Após geração do boleto pelo bot, um email é enviado para algum email desejado utilizando a [SendGrid API](https://docs.sendgrid.com/pt-br/for-developers/sending-email/api-getting-started). Esse email contém o boleto no formato HTML como anexo e o código de barras bem como a categoria selecionada no corpo do email caso ele tenha sido executado com sucesso. Caso algum erro tenha ocorrido, um email também é enviado ao usuário informando que algum erro ocorreu durante a execução do programa.

## Observações técnicas

O site requer que o usuário resolva um CAPTCHA, por conta disso, é utilizado aqui o serviço [2Captcha](https://2captcha.com/) que é especializado em resolver esse tipo de verificação.

O bot foi criado para funcionar na AWS cloud de tempos em tempos e serão apresentadas formas de fazer isso em seguida. Contudo, ele pode ser adaptado para funcionar em outras plataformas.

Para passar da tela em que o CAPTCHA é verificado, é utilizado o módulo [Selenium](https://selenium-python.readthedocs.io/) do python. Os outros passos são realizados através de requisições.

## Passos para o deploy na AWS

### Faça deploy da imagem na Amazon ECR

#### Opção 1 (Mais simples, utiliza imagem pública gerada através do GitHub Actions)

- Crie um repositório **privado** na Amazon ECR.

- Dê pull na imagem disponibilizada publicamente

  `docker pull public.ecr.aws/p2m9w2p6/inss-gps-bot:latest`

- Entre em `Amazon ECR > Repositories > MY_REPOSITORY_NAME`. Clique em seguida em "View push commands". Ela será útil nos próximos passos.

- Identifique a versão que acabou de ser baixada no passo anterior, executando o seguinte comando:

  `docker tag IMAGE_ID AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/MY_REPOSITORY_NAME:TAG`

  O valor `IMAGE_ID` pode ser encontrado executando: `docker images`, após o pull ser concluído. Ela terá como `REPOSITORY` o valor `inss-gps-bot`. A URL do repositório pode ser encontrada no passo 3 em "View push commands".

- Autentique o Docker client executando o seguinte comando, presente no passo 1 em "View push comands":

  `aws ecr get-login-password --region AWS_REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com`

- Dê push na imagem AWS que foi baixada no início no seu repositório privado.

  `docker push AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/MY_REPOSITORY_NAME:TAG`

#### Opção 2 (Um pouco mais complexa, gera sua própria Docker image)

- Caso prefira, para ajudar nesse passo, assista o seguinte vídeo: https://www.youtube.com/watch?v=yv8-Si5AB3U.

- Crie um repositório **privado** na Amazon ECR.

- Clone esse repositório localmente (através do `git clone`)

- Crie e configure um novo usuário, utilizando o serviço "IAM".
  - Adicione Access Key como tipo de credencial AWS.
  - Clique em "Attach existing policies directly" e adicione as seguintes políticas:
    - AmazonEC2ContainerRegistryFullAccess
    - AdministratorAccess
    - AmazonEC2ContainerRegistryPowerUser
    - AmazonEC2ContainerRegistryReadOnly
  - Siga e crie o usuário
  - Guarde a "Access key ID" e a "Secret access key"
- Em `Seu repositório no GitHub > Settings > Secrets > Actions > New repository secret`, adicione as seguintes variáveis:

  - Name: `AWS_ACCESS_KEY_ID`, Secret: Valor obtido no passo anterior em "Access key ID".
  - Name: `AWS_SECRET_ACCESS_KEY`, Secret: Valor obtido no passo anterior em "Secret access key".
  - Name: `AWS_REGION`, Secret: Valor presente no canto superior direito da página da AWS. Ex: us-east-1
  - Name: `FUNCTION_ARN_NAME`, Secret: Valor obtido no próximo passo, após criar a função lambda.
  - Name: `REPOSITORY`, Secret: Nome do repositório lambda obtido no próximo passo, após a criação da função.

- Em `.github/workflows/aws.yml`, apague os seguintes "steps":

  - Login to Amazon ECR Public
  - Build, tag, and push docker image to Amazon ECR Public
  - Delete untagged images

- Pronto, agora ao dar qualquer push ao seu repositório, ele cumprirá os passos presentes na GitHub Actions de:
  - Fazer build e push da imagem Docker no repositório ECR.
  - Atualizar a URL da imagem Docker para a nova gerada no passo anterior.
  - Apagar todas as imagens Docker antigas (sem tag) do repositório ECR de forma a manter somente uma lá.

### Configure uma função AWS Lambda

- Crie uma função AWS Lambda.

  - Selecione a opção: "Container Image".
  - Nomeie a função como preferir.
  - Selecione a imagem criada no passo anterior.
  - Arquitetura: x86_64.

- Selecione a aba Configuração.

  - Selecione a aba Configuração Geral
    - Aumente os limites de memória, armazenamento e timeout para o máximo disponível.
  - Selecione a aba Variáveis de Ambiente
    - Adicione as Variáveis de Ambiente e seus valores. Veja o arquivo `.secret_example.env` e adicione todos as chaves e valores presentes lá como instruído. Caso tenha escolhido a opção 1 na seção anterior você não vai precisar alterar esse arquivo em nada, ele servirá só pra auxiliar nesse passo.

- Para testar se a função está funcionando corretamente basta entrar na aba Test e criar um evento teste para rodar a função.

### Crie eventos recorrentes para rodar a função em intervalos de tempo pré-definidos

- Entre no serviço: "EventBridge".

- Clique em: "Create rule".

- Crie uma regra do tipo "Schedule".

- Defina uma expressão do tipo [cron](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html).

- Selecione o serviço "Lambda Function" e escolha a função criada no passo anterior.

- Confirme o evento.

- Pronto, agora no intervalo de tempo pré-definido no evento criado, a função será executada regularmente.

### Extra

#### Como testar a imagem Docker localmente? (Caso tenha escolhido a opção 2 de criar um repositório Github e gerar a Docker image manualmente)

- Altere o arquivo `.secret_example.env` para `.secret.env` e o preencha como instruído.
- Construa a imagem: `docker compose build`
- Rode a imagem: `docker run -p 9000:8080 --env-file .secret.env MY_REPOSITORY_NAME:latest`
- Rode a função através do seguinte request em outro terminal:

  `curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

  Veja [esse tutorial](https://docs.aws.amazon.com/lambda/latest/dg/images-test.html) para mais informações.
