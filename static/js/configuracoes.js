// ============================================================
// FLASHMATTY - CONFIGURAÇÕES
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        // ====================================================
        // AVISO DE CONFIGURAÇÃO SALVA
        // ====================================================

        const aviso =
            document.getElementById(
                "configSalva"
            );


        let timerAviso = null;


        function mostrarAviso(
            mensagem = "✓ Configuração salva"
        ) {

            if (!aviso) {
                return;
            }


            aviso.textContent =
                mensagem;


            aviso.classList.remove(
                "hidden"
            );


            clearTimeout(
                timerAviso
            );


            timerAviso =
                setTimeout(
                    () => {

                        aviso.classList.add(
                            "hidden"
                        );

                    },
                    1500
                );

        }


        // ====================================================
        // TEMA
        // ====================================================

        const tema =
            document.getElementById(
                "temaAplicativo"
            );


        const painelPersonalizado =
            document.getElementById(
                "painelTemaPersonalizado"
            );


        const corPrimaria =
            document.getElementById(
                "corPrimaria"
            );


        const corFundo =
            document.getElementById(
                "corFundo"
            );


        const corCard =
            document.getElementById(
                "corCard"
            );


        const corTexto =
            document.getElementById(
                "corTexto"
            );


        const corSecundaria =
            document.getElementById(
                "corSecundaria"
            );


        const corBorda =
            document.getElementById(
                "corBorda"
            );


        const preview =
            document.getElementById(
                "previewTema"
            );


        const previewCard =
            document.getElementById(
                "previewCard"
            );


        const previewTitulo =
            document.getElementById(
                "previewTitulo"
            );


        const previewTexto =
            document.getElementById(
                "previewTexto"
            );


        const previewBotao =
            document.getElementById(
                "previewBotao"
            );


        const salvarTema =
            document.getElementById(
                "salvarTemaPersonalizado"
            );


        const restaurarTema =
            document.getElementById(
                "restaurarTemaPersonalizado"
            );


        // ====================================================
        // PEGAR CORES PERSONALIZADAS
        // ====================================================

        function pegarCores() {

            return {

                primaria:
                    corPrimaria?.value
                    ||
                    "#8b5cf6",

                fundo:
                    corFundo?.value
                    ||
                    "#111827",

                card:
                    corCard?.value
                    ||
                    "#1f2937",

                superficie:
                    corBorda?.value
                    ||
                    "#374151",

                texto:
                    corTexto?.value
                    ||
                    "#f9fafb",

                secundario:
                    corSecundaria?.value
                    ||
                    "#9ca3af",

                borda:
                    corBorda?.value
                    ||
                    "#374151"

            };

        }


        // ====================================================
        // PRÉ-VISUALIZAÇÃO
        // ====================================================

        function atualizarPreview() {

            if (
                !preview
                ||
                !previewCard
            ) {

                return;

            }


            const cores =
                pegarCores();


            preview.style.background =
                cores.fundo;


            preview.style.borderColor =
                cores.borda;


            previewCard.style.background =
                cores.card;


            previewCard.style.borderColor =
                cores.borda;


            if (previewTitulo) {

                previewTitulo.style.color =
                    cores.texto;

            }


            if (previewTexto) {

                previewTexto.style.color =
                    cores.secundario;

            }


            if (previewBotao) {

                previewBotao.style.background =
                    cores.primaria;

                previewBotao.style.color =
                    "#ffffff";

            }

        }


        // ====================================================
        // CARREGAR CORES SALVAS
        // ====================================================

        function carregarCoresPersonalizadas() {

            if (
                !window.FlashMattyTema
            ) {

                console.warn(
                    "FlashMattyTema não foi carregado."
                );

                return;

            }


            const cores =
                window.FlashMattyTema
                    .obterPersonalizado();


            if (corPrimaria) {

                corPrimaria.value =
                    cores.primaria;

            }


            if (corFundo) {

                corFundo.value =
                    cores.fundo;

            }


            if (corCard) {

                corCard.value =
                    cores.card;

            }


            if (corTexto) {

                corTexto.value =
                    cores.texto;

            }


            if (corSecundaria) {

                corSecundaria.value =
                    cores.secundario;

            }


            if (corBorda) {

                corBorda.value =
                    cores.borda;

            }


            atualizarPreview();

        }


        // ====================================================
        // NORMALIZAR TEMA ANTIGO
        // ====================================================

        function obterTemaAtual() {

            let atual =
                localStorage.getItem(
                    "flashmatty_tema"
                )
                ||
                "dark";


            if (
                ![
                    "dark",
                    "light",
                    "custom"
                ].includes(
                    atual
                )
            ) {

                atual =
                    "dark";

            }


            return atual;

        }


        // ====================================================
        // INICIALIZAR TEMA
        // ====================================================

        if (
            tema
            &&
            window.FlashMattyTema
        ) {

            const atual =
                obterTemaAtual();


            tema.value =
                atual;


            painelPersonalizado
                ?.classList.toggle(
                    "hidden",
                    atual !== "custom"
                );


            carregarCoresPersonalizadas();

        }


        // ====================================================
        // TROCAR TEMA
        // ====================================================

        tema?.addEventListener(
            "change",
            () => {

                if (
                    !window.FlashMattyTema
                ) {

                    return;

                }


                const valor =
                    tema.value;


                if (
                    valor === "custom"
                ) {

                    painelPersonalizado
                        ?.classList.remove(
                            "hidden"
                        );


                    carregarCoresPersonalizadas();


                    window.FlashMattyTema
                        .aplicar(
                            "custom"
                        );

                } else {

                    painelPersonalizado
                        ?.classList.add(
                            "hidden"
                        );


                    window.FlashMattyTema
                        .aplicar(
                            valor
                        );

                }


                mostrarAviso(
                    "✓ Tema alterado"
                );

            }
        );


        // ====================================================
        // ALTERAR PREVIEW EM TEMPO REAL
        // ====================================================

        [
            corPrimaria,
            corFundo,
            corCard,
            corTexto,
            corSecundaria,
            corBorda

        ].forEach(
            input => {

                input?.addEventListener(
                    "input",
                    atualizarPreview
                );

            }
        );


        // ====================================================
        // SALVAR TEMA PERSONALIZADO
        // ====================================================

        salvarTema?.addEventListener(
            "click",
            () => {

                if (
                    !window.FlashMattyTema
                ) {

                    return;

                }


                window.FlashMattyTema
                    .salvarPersonalizado(
                        pegarCores()
                    );


                if (tema) {

                    tema.value =
                        "custom";

                }


                mostrarAviso(
                    "🎨 Tema personalizado salvo"
                );

            }
        );


        // ====================================================
        // RESTAURAR TEMA PERSONALIZADO
        // ====================================================

        restaurarTema?.addEventListener(
            "click",
            () => {

                if (
                    !window.FlashMattyTema
                ) {

                    return;

                }


                window.FlashMattyTema
                    .restaurarPersonalizado();


                carregarCoresPersonalizadas();


                if (tema) {

                    tema.value =
                        "custom";

                }


                mostrarAviso(
                    "↺ Cores restauradas"
                );

            }
        );


        // ====================================================
        // ÁUDIO
        // ====================================================

        const volume =
            document.getElementById(
                "volumeAplicativo"
            );


        const volumeValor =
            document.getElementById(
                "volumeValor"
            );


        const sonsAtivados =
            document.getElementById(
                "sonsAtivados"
            );


        const testarSom =
            document.getElementById(
                "testarSom"
            );


        // ====================================================
        // CARREGAR VOLUME
        // ====================================================

        const volumeSalvo =
            Math.max(
                0,
                Math.min(
                    100,
                    Number(
                        localStorage.getItem(
                            "flashmatty_volume"
                        )
                        ??
                        70
                    )
                )
            );


        if (volume) {

            volume.value =
                volumeSalvo;

        }


        if (volumeValor) {

            volumeValor.textContent =
                `${volumeSalvo}%`;

        }


        // ====================================================
        // CARREGAR SOM ON/OFF
        // ====================================================

        if (sonsAtivados) {

            sonsAtivados.checked =
                localStorage.getItem(
                    "flashmatty_sons"
                )
                !==
                "false";

        }


        // ====================================================
        // ALTERAR VOLUME
        // ====================================================

        volume?.addEventListener(
            "input",
            () => {

                const valor =
                    Number(
                        volume.value
                    );


                localStorage.setItem(
                    "flashmatty_volume",
                    String(
                        valor
                    )
                );


                if (volumeValor) {

                    volumeValor.textContent =
                        `${valor}%`;

                }

            }
        );


        volume?.addEventListener(
            "change",
            () => {

                mostrarAviso(
                    `🔊 Volume: ${volume.value}%`
                );

            }
        );


        // ====================================================
        // ATIVAR / DESATIVAR SOM
        // ====================================================

        sonsAtivados?.addEventListener(
            "change",
            () => {

                localStorage.setItem(
                    "flashmatty_sons",
                    String(
                        sonsAtivados.checked
                    )
                );


                mostrarAviso(

                    sonsAtivados.checked
                        ?
                        "🔊 Sons ativados"
                        :
                        "🔇 Sons desativados"

                );

            }
        );


        // ====================================================
        // TESTAR SOM
        // ====================================================

        testarSom?.addEventListener(
            "click",
            async () => {

                const ativo =
                    localStorage.getItem(
                        "flashmatty_sons"
                    )
                    !==
                    "false";


                const vol =
                    Number(
                        localStorage.getItem(
                            "flashmatty_volume"
                        )
                        ??
                        70
                    );


                if (!ativo) {

                    mostrarAviso(
                        "🔇 Os sons estão desativados"
                    );

                    return;

                }


                if (vol <= 0) {

                    mostrarAviso(
                        "🔇 O volume está em 0%"
                    );

                    return;

                }


                if (
                    typeof window.ativarAudio
                    ===
                    "function"
                ) {

                    await window.ativarAudio();

                }


                if (
                    typeof window.somMoeda
                    ===
                    "function"
                ) {

                    window.somMoeda();

                } else if (
                    typeof window.somClique
                    ===
                    "function"
                ) {

                    window.somClique();

                }

            }
        );


        // ====================================================
        // ACESSIBILIDADE
        // ====================================================

        const reduzirAnimacoes =
            document.getElementById(
                "reduzirAnimacoes"
            );


        const textoGrande =
            document.getElementById(
                "textoGrande"
            );


        // ====================================================
        // CARREGAR ACESSIBILIDADE
        // ====================================================

        if (reduzirAnimacoes) {

            reduzirAnimacoes.checked =
                localStorage.getItem(
                    "flashmatty_reduzir_animacoes"
                )
                ===
                "true";

        }


        if (textoGrande) {

            textoGrande.checked =
                localStorage.getItem(
                    "flashmatty_texto_grande"
                )
                ===
                "true";

        }


        // ====================================================
        // REDUZIR ANIMAÇÕES
        // ====================================================

        reduzirAnimacoes?.addEventListener(
            "change",
            () => {

                const ativo =
                    reduzirAnimacoes.checked;


                localStorage.setItem(
                    "flashmatty_reduzir_animacoes",
                    String(
                        ativo
                    )
                );


                document.documentElement
                    .classList.toggle(
                        "reduzir-animacoes",
                        ativo
                    );


                mostrarAviso(

                    ativo
                        ?
                        "♿ Animações reduzidas"
                        :
                        "✓ Animações normais"

                );

            }
        );


        // ====================================================
        // TEXTO GRANDE
        // ====================================================

        textoGrande?.addEventListener(
            "change",
            () => {

                const ativo =
                    textoGrande.checked;


                localStorage.setItem(
                    "flashmatty_texto_grande",
                    String(
                        ativo
                    )
                );


                document.documentElement
                    .classList.toggle(
                        "texto-grande",
                        ativo
                    );


                mostrarAviso(

                    ativo
                        ?
                        "🔎 Texto maior ativado"
                        :
                        "✓ Texto normal"

                );

            }
        );


        // ====================================================
        // MODAL DE INFORMAÇÕES
        // ====================================================

        const modal =
            document.getElementById(
                "modalInfo"
            );


        const modalTitulo =
            document.getElementById(
                "modalTitulo"
            );


        const modalConteudo =
            document.getElementById(
                "modalConteudo"
            );


        const fecharModal =
            document.getElementById(
                "fecharModalInfo"
            );


        const informacoes = {


            creditos: {

                titulo:
                    " Créditos",

                conteudo:
                    `
                    <p>
                       Desenvolvimento:
                        <strong>Programador : Sena  </strong>.
                         <strong>Designer : yure </strong>.

                    </p>

                   

                    
                    
                    `

            },


            privacidade: {

                titulo:
                    " Política de Privacidade",

                conteudo:
                    `
                    <p>
                        O FlashMatty utiliza dados necessários
                        ao funcionamento da conta, incluindo
                        nome, nome de usuário, progresso,
                        amizades e preferências.
                    </p>

                    <p>
                        Preferências como tema, volume e
                        acessibilidade podem ser armazenadas
                        localmente no dispositivo.
                    </p>

                    <p>
                        Fotos de perfil enviadas pelo usuário
                        podem ser armazenadas para utilização
                        nos recursos sociais da plataforma.
                    </p>

                    <p>
                        Antes da publicação oficial do
                        aplicativo, esta política deverá ser
                        revisada para refletir exatamente o
                        tratamento real dos dados.
                    </p>
                    `

            },


            termos: {

                titulo:
                    " Termos de Uso",

                conteudo:
                    `
                    <p>
                        O FlashMatty deve ser utilizado de
                        maneira adequada e respeitosa.
                    </p>

                    <p>
                        Os recursos sociais e multiplayer não
                        devem ser utilizados para prejudicar,
                        ameaçar ou assediar outros usuários.
                    </p>

                    <p>
                        Funcionalidades e regras podem ser
                        atualizadas conforme o desenvolvimento
                        da plataforma.
                    </p>
                    `

            }

        };


        // ====================================================
        // ABRIR MODAL
        // ====================================================

        document
            .querySelectorAll(
                "[data-abrir-info]"
            )
            .forEach(
                botao => {

                    botao.addEventListener(
                        "click",
                        () => {

                            const chave =
                                botao.dataset
                                    .abrirInfo;


                            const dados =
                                informacoes[
                                    chave
                                ];


                            if (
                                !dados
                                ||
                                !modal
                                ||
                                !modalTitulo
                                ||
                                !modalConteudo
                            ) {

                                return;

                            }


                            modalTitulo.textContent =
                                dados.titulo;


                            modalConteudo.innerHTML =
                                dados.conteudo;


                            modal.classList.remove(
                                "hidden"
                            );

                        }
                    );

                }
            );


        // ====================================================
        // FECHAR MODAL
        // ====================================================

        function fecharInformacao() {

            modal?.classList.add(
                "hidden"
            );

        }


        fecharModal?.addEventListener(
            "click",
            fecharInformacao
        );


        modal?.addEventListener(
            "click",
            event => {

                if (
                    event.target
                    ===
                    modal
                ) {

                    fecharInformacao();

                }

            }
        );


        document.addEventListener(
            "keydown",
            event => {

                if (
                    event.key
                    ===
                    "Escape"
                ) {

                    fecharInformacao();

                }

            }
        );


        // ====================================================
        // DEBUG
        // ====================================================

        console.log(
            "⚙️ Configurações FlashMatty carregadas."
        );


        console.log(
            "🎨 Tema:",
            obterTemaAtual()
        );


        console.log(
            "🔊 Volume:",
            `${volumeSalvo}%`
        );

    }
);