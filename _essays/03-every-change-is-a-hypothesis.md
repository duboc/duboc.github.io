---
layout: essay
generated: true
permalink: "/essays/every-change-is-a-hypothesis/"
title: "Every Change Is a Hypothesis"
title_en: "Every Change Is a Hypothesis"
title_pt: "Toda Mudança É uma Hipótese"
description: "Most of us are playing slot machines and calling it engineering."
description_pt: "Quase todos estamos jogando caça-níquel e chamando isso de engenharia."
date: 2026-09-25
series: the-future-of-software
part: 1
order: 3
---

<section lang="en" markdown="1">

Most of us are playing slot machines and calling it engineering.

Software grew up on determinism. Run the test once, and if it passes today it will pass tomorrow. CI/CD pipelines, regression suites, the entire rhythm of fast iteration rests on that promise. Put a model inside the workflow and the promise breaks. The same prompt returns different answers. Change one token and, formally, anything can happen, even if it rarely does.

In a probabilistic system, every change is a hypothesis test. That sounds academic until you do the math. Detecting a 1% improvement with a 2% standard deviation, under assumptions kinder than reality, takes around 52 paired runs. The samples you need grow with the square of noise over effect size. Who runs 52 trials before merging a prompt tweak? Almost nobody. We merge on three to five runs and a good feeling.

That is not always wrong. The danger is subtler: weeks of iterated changes, each one feeling like progress, adding up to nothing.

So borrow from the people who have always lived with noise. Pair your experiments so both arms face the same interference, the way farmers test fertilizer on neighboring plots. Stack several suspected improvements and measure them together. Build small benchmarks for speed and big ones to keep the small ones honest.

Feynman said it first: you must not fool yourself, and you are the easiest person to fool.

Congratulations. You are a scientist now.

</section>

<section lang="pt-BR" markdown="1">

Quase todos estamos jogando caça-níquel e chamando isso de engenharia.

O software cresceu em cima do determinismo. Rode o teste uma vez e, se ele passa hoje, vai passar amanhã. Pipelines de CI/CD, suítes de regressão, todo o ritmo de iteração rápida depende dessa promessa. Coloque um modelo dentro do fluxo e a promessa quebra. O mesmo prompt devolve respostas diferentes. Troque um token e, formalmente, qualquer coisa pode acontecer, mesmo que quase nunca aconteça.

Num sistema probabilístico, toda mudança é um teste de hipótese. Parece acadêmico até você fazer a conta. Detectar uma melhoria de 1% com desvio-padrão de 2%, sob premissas mais gentis que a realidade, exige cerca de 52 rodadas pareadas. As amostras necessárias crescem com o quadrado do ruído dividido pelo tamanho do efeito. Quem roda 52 testes antes de fazer merge de um ajuste de prompt? Quase ninguém. Fazemos merge com três a cinco rodadas e uma boa sensação.

Isso nem sempre é errado. O perigo é mais sutil: semanas de mudanças iteradas, cada uma com cara de progresso, somando zero.

Então pegue emprestado de quem sempre conviveu com ruído. Pareie seus experimentos para que os dois lados enfrentem a mesma interferência, como agricultores testando adubo em canteiros vizinhos. Empilhe várias melhorias suspeitas e meça todas juntas. Monte benchmarks pequenos para ter velocidade e grandes para manter os pequenos honestos.

Feynman disse primeiro: você não pode enganar a si mesmo, e você é a pessoa mais fácil de enganar.

Parabéns. Agora você é cientista.

</section>

<aside class="sources" markdown="1">

<p class="sources-label"><span lang="en">Based on</span><span lang="pt-BR">Baseado em</span></p>

- Thomas Dullien, [*An age of experimentation*](https://thomasdullien.github.io/about/slides/An-age-of-experimentation-BlueHat-Asia-2026.pdf), talk at Microsoft BlueHat Asia, Singapore, September 2026.

</aside>
