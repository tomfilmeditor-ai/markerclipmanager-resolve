MarkerClipManager — Gerenciador de Marcadores de Timeline e Clipes para DaVinci Resolve
=======================================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.8
MIT License — see the script header

O QUE FAZ
---------
Uma única janela para visualizar e gerenciar todos os marcadores em uma timeline do Resolve: 
marcadores de régua (nível de timeline) e marcadores colocados em clipes individuais,
em todas as trilhas de vídeo e áudio.

Para cada marcador mostra: gráfico de marcador (mesma forma nativa que Resolve),
trilha, TC entrada, TC saída, duração, cor, nome, palavra-chave, nota.

RECURSOS
--------
- Selecione um ou mais marcadores e mude a cor, mude a faixa (inclusive
  de/para a régua "TIMELINE"), exclua
- Edite Nome, Palavra-chave e Nota diretamente na tabela (clique duplo),
  mesmo em vários marcadores selecionados de uma vez
- A tecla Delete faz o mesmo que o botão Excluir, com uma confirmação que você
  pode desativar
- Desfazer e refazer com Cmd+Z / Ctrl+Z, além de um painel History: clique
  duplo em uma etapa anterior para voltar direto a ela. Cobre apenas a sessão
  atual e é limpo ao fechar o script
- Filtre por cor, faixa, autor/nome ou palavra-chave
- Exporte e importe marcadores em CSV
- Clique em uma linha: o cabeçote de reprodução salta para aquele marcador
- Interface disponível em 12 idiomas: inicia no idioma do seu sistema quando há
  correspondência, caso contrário em inglês, e você pode mudá-lo pelo menu no
  alto da janela (tem efeito ao reiniciar o script)

REQUISITOS
----------
- DaVinci Resolve 19/20 (macOS)
- Python 3 instalado no sistema
- PySide6 (instalado automaticamente pelo script de configuração abaixo — nenhuma
  etapa manual necessária)

INSTALAÇÃO (uma única vez)
--------------------------
1. Baixe o instalador para o seu sistema
2. macOS: CLIQUE COM O BOTÃO DIREITO no arquivo .command e escolha "Abrir" —
   não clique duplo, que o macOS bloqueia porque o arquivo não é assinado com
   um certificado de desenvolvedor Apple
   Windows: clique duplo no arquivo .cmd; se o SmartScreen avisar, escolha
   "Mais informações" e depois "Executar assim mesmo"
3. O instalador copia os arquivos e em seguida prepara o ambiente Python de que
   o script precisa (esta parte requer conexão com a internet e leva cerca de
   um minuto)
4. Se essa segunda parte falhar — sem conexão, ou sem Python — os arquivos
   ficam instalados corretamente mesmo assim: abra a pasta instalada e execute
   "MarkerClipManager_Setup.command" (macOS) ou
   "MarkerClipManager_Setup_Windows.cmd" (Windows) quando puder
5. Pronto. As atualizações são instaladas do mesmo modo, por cima da versão
   anterior, e suas configurações permanecem intactas

USO
---
No DaVinci Resolve: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(o script está na subpasta "MarkerClipManager" dentro de Comp, portanto aparece
no menu como um submenu com o mesmo nome)

LIMITAÇÕES CONHECIDAS
---------------------
- O marcador na tabela é um ícone recriado desenhado pelo script, não
  o ícone oficial do Resolve (não exposto pela API). As cores são os
  valores hexadecimais exatos fornecidos pelo usuário — apenas a forma
  do ícone permanece uma aproximação
- "Palavra-chave" não é um campo de marcador nativo do Resolve: é armazenado
  em um campo de marcador interno (customData), invisível ao painel Marker
  nativo do Resolve — legível/gravável apenas por este script
- Timecode lê fps e modo Drop Frame/Non-Drop Frame diretamente da timeline
  ativa do projeto (29.97 e 59.94 DF tratados corretamente com o algoritmo
  SMPTE padrão); em fps não-padrão a matemática permanece aproximada
- Importação/exportação de EDL não é tratada por este script: use o
  recurso nativo do Resolve (Timeline > Markers > Export/Import)
- Mover um marcador para uma trilha de vídeo/áudio requer que um clipe já
  exista nessa posição

SUPORTE
-------
Relatórios de bug: use o botão 🐛 no app (abre um email pré-preenchido para
tomfilmeditor.tools@gmail.com)
Se deseja apoiar o desenvolvimento: botão ☕ no app, ou
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
