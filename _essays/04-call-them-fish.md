---
layout: essay
generated: true
permalink: "/essays/call-them-fish/"
title: "Call Them Fish"
title_en: "Call Them Fish"
title_pt: "Chame de Peixe"
description: "Maybe we should stop calling them bugs and start calling them fish."
description_pt: "Talvez devêssemos parar de chamar de bugs e começar a chamar de peixes."
date: 2026-09-25
series: the-future-of-software
part: 1
order: 4
---

<section lang="en" markdown="1">

Maybe we should stop calling them bugs and start calling them fish.

LLM code review behaves less like a static analyzer and more like fuzzing. Run it twice on the same code and you get two different sets of findings. Tweak the prompt and the set changes again. Ship a new model generation and it changes once more. Like fuzzing, it is never done.

That breaks the way we usually measure security. A codebase with a hundred known bugs sounds like a clean benchmark, until you notice an agent's run is path-dependent: skip one file and a dozen findings vanish together. The bugs are not independent trials, and the confidence intervals we draw around them are narrower than the truth.

Fishery management has lived with this for a century. Nobody knows how many fish are in the ocean. Fish are born at some rate and caught at some rate. You cannot count the stock; you can only track effort and catch. Better boats catch more, and the stock thins.

Security looks the same. Bugs are introduced at a rate and removed at a rate. Nobody knows the total. So the honest metric is not "are we clean?" It is useful discoveries per dollar of compute. Watch it fall over time, and hope it falls for attackers too.

You will never know whether a tuna is hiding somewhere. The ocean is too vast.

The goal is to make fishing expensive.

</section>

<section lang="pt-BR" markdown="1">

Talvez devêssemos parar de chamar de bugs e começar a chamar de peixes.

O code review com LLM se comporta menos como um analisador estático e mais como fuzzing. Rode duas vezes no mesmo código e você recebe dois conjuntos diferentes de achados. Ajuste o prompt e o conjunto muda de novo. Lance uma nova geração de modelo e ele muda mais uma vez. Como o fuzzing, nunca termina.

Isso quebra o jeito como costumamos medir segurança. Uma base de código com cem bugs conhecidos parece um benchmark limpo, até você notar que a execução de um agente depende do caminho: ele pula um arquivo e uma dúzia de achados some junto. Os bugs não são tentativas independentes, e os intervalos de confiança que desenhamos em volta deles são mais estreitos que a verdade.

A gestão pesqueira convive com isso há um século. Ninguém sabe quantos peixes existem no oceano. Peixes nascem num ritmo e são pescados em outro. Não dá para contar o estoque; só dá para acompanhar esforço e captura. Barcos melhores pescam mais, e o estoque diminui.

Segurança é igual. Bugs entram num ritmo e saem em outro. Ninguém sabe o total. Então a métrica honesta não é "estamos limpos?". É achados úteis por dólar de compute. Acompanhe essa curva cair com o tempo, e torça para ela cair para os atacantes também.

Você nunca vai saber se tem um atum escondido em algum lugar. O oceano é grande demais.

O objetivo é deixar a pesca cara.

</section>

<aside class="sources" markdown="1">

<p class="sources-label"><span lang="en">Based on</span><span lang="pt-BR">Baseado em</span></p>

- Thomas Dullien, [*An age of experimentation*](https://thomasdullien.github.io/about/slides/An-age-of-experimentation-BlueHat-Asia-2026.pdf), talk at Microsoft BlueHat Asia, Singapore, September 2026.

</aside>
