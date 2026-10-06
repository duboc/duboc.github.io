---
layout: essay
generated: true
permalink: "/essays/the-last-code-review/"
title: "The Last Code Review"
title_en: "The Last Code Review"
title_pt: "O Último Code Review"
description: "Code review is already dead. The news is just unevenly distributed."
description_pt: "O code review já morreu. A notícia só não chegou a todos ao mesmo tempo."
date: 2026-09-25
series: the-future-of-software
part: 2
order: 7
---

<section lang="en" markdown="1">

Code review is already dead. The news is just unevenly distributed.

For decades, a second pair of human eyes on every change was how teams bought quality, shared understanding and satisfied compliance. Those reasons were real. They are also dissolving one by one.

Quality is moving to machines that read faster and more patiently than any reviewer: LLM-as-judge review, static analysis, automated reasoning, property-based testing, deterministic simulation, model-guided fuzzing, correct-by-construction design. Together they already catch more, big and small, than a tired engineer scrolling a diff at 6 p.m. The idea that humans will reliably spot the rare issue all of that missed is a fantasy. Even unit tests start to look like training wheels once the rider stops falling. And open source's old promise still holds: enough eyeballs make every bug shallow. The eyeballs are just artificial now.

The mixed mode, humans spot-checking with tools at their side, is useful today and temporary tomorrow.

The harder question is learning. Review was where juniors absorbed taste, one comment at a time. That school does not vanish. It moves up a layer, from the code to the specification, the requirements, the feedback. Mechanical sympathy for the layers below stays valuable. Daily work happens above them.

Humans will still review. They will review systems and how they compose.

Nobody will read the diff.

</section>

<section lang="pt-BR" markdown="1">

O code review já morreu. A notícia só não chegou a todos ao mesmo tempo.

Por décadas, um segundo par de olhos humanos em cada mudança foi como times compraram qualidade, compartilharam entendimento e atenderam compliance. Esses motivos eram reais. E estão se dissolvendo um a um.

A qualidade está migrando para máquinas que leem mais rápido e com mais paciência do que qualquer revisor: review com LLM-as-judge, análise estática, automated reasoning, property-based testing, deterministic simulation, fuzzing guiado por modelo, correct-by-construction. Juntas, elas já pegam mais problemas, grandes e pequenos, do que um engenheiro cansado rolando um diff às 18h. A ideia de que humanos vão encontrar com confiança o problema raro que tudo isso deixou passar é fantasia. Até o teste unitário começa a parecer rodinha de bicicleta quando o ciclista para de cair. E a velha promessa do open source continua valendo: com olhos suficientes, todo bug é raso. Os olhos só ficaram artificiais.

O modo misto, humanos conferindo por amostragem com ferramentas ao lado, é útil hoje e passageiro amanhã.

A pergunta difícil é o aprendizado. O review era onde o júnior absorvia gosto, um comentário por vez. Essa escola não some. Ela sobe de camada: do código para a especificação, os requisitos, o feedback. Ter mechanical sympathy pelas camadas de baixo continua valendo muito. O trabalho do dia a dia acontece acima delas.

Humanos vão continuar revisando. Vão revisar sistemas e como eles se compõem.

Ninguém vai ler o diff.

</section>
