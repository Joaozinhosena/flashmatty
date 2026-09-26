(() => {
  "use strict";

  function atualizarStatus(usuarioId, online) {
    document.querySelectorAll(`[data-online-user="${usuarioId}"]`).forEach(el => {
      el.dataset.online = online ? "1" : "0";
      el.textContent = online ? "● Online" : "● Offline";
    });
  }

  function criarToast(mensagem, opcoes = {}) {
    const toast = document.createElement("div");
    Object.assign(toast.style, {
      position: "fixed", right: "18px", bottom: "18px", zIndex: "99999",
      width: "min(380px, calc(100vw - 36px))", background: "#0f172a",
      color: "#fff", border: "1px solid #334155", borderRadius: "18px",
      padding: "16px", boxShadow: "0 20px 50px rgba(0,0,0,.35)",
      fontFamily: "system-ui, sans-serif"
    });

    const texto = document.createElement("div");
    texto.textContent = mensagem;
    texto.style.fontWeight = "800";
    toast.appendChild(texto);

    if (opcoes.textoBotao && typeof opcoes.aoClicar === "function") {
      const botao = document.createElement("button");
      botao.type = "button";
      botao.textContent = opcoes.textoBotao;
      Object.assign(botao.style, {
        marginTop: "12px", background: "#4f46e5", color: "white", border: "0",
        borderRadius: "12px", padding: "10px 14px", fontWeight: "900", cursor: "pointer"
      });
      botao.addEventListener("click", () => {
        opcoes.aoClicar();
        toast.remove();
      });
      toast.appendChild(botao);
    }

    document.body.appendChild(toast);
    setTimeout(() => { if (toast.isConnected) toast.remove(); }, opcoes.duracao || 6000);
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (typeof window.io !== "function") {
      console.warn("Socket.IO não foi carregado; presença social desativada.");
      return;
    }

    const socket = window.io();
    window.flashSocialSocket = socket;

    function enviarHeartbeat() {
      if (socket.connected) socket.emit("social_presenca");
    }

    function idsVisiveis() {
      return [...new Set(
        Array.from(document.querySelectorAll("[data-online-user]"))
          .map(el => Number(el.dataset.onlineUser))
          .filter(Number.isFinite)
      )];
    }

    function consultarPresenca() {
      const usuarios = idsVisiveis();
      if (usuarios.length && socket.connected) {
        socket.emit("social_consultar_presenca", { usuarios });
      }
    }

    socket.on("connect", () => {
      enviarHeartbeat();
      consultarPresenca();
    });

    setInterval(enviarHeartbeat, 20000);
    setInterval(consultarPresenca, 25000);

    socket.on("social_status", dados => {
      atualizarStatus(dados.usuario_id, Boolean(dados.online));
    });

    socket.on("social_presenca_resultado", resultado => {
      Object.entries(resultado || {}).forEach(([id, online]) => atualizarStatus(id, Boolean(online)));
    });

    document.querySelectorAll("[data-desafiar-usuario]").forEach(botao => {
      botao.addEventListener("click", () => {
        const usuarioId = Number(botao.dataset.desafiarUsuario);
        if (!Number.isFinite(usuarioId)) return;
        if (typeof window.somClique === "function") window.somClique();
        socket.emit("social_desafiar", { usuario_id: usuarioId });
      });
    });

    socket.on("social_desafio_resultado", dados => {
      criarToast(dados.mensagem || "Desafio processado.");
    });

    socket.on("social_desafio_recebido", dados => {
      if (typeof window.somConcluido === "function") window.somConcluido();
      criarToast(`${dados.nome} desafiou você para uma partida! 🎮`, {
        textoBotao: "Aceitar desafio",
        duracao: 15000,
        aoClicar: () => {
          socket.emit("social_desafio_aceito", { desafiante_id: dados.desafiante_id });
          window.location.href = dados.url_multiplayer;
        }
      });
    });

    socket.on("social_desafio_aceito", dados => {
      if (typeof window.somConcluido === "function") window.somConcluido();
      criarToast(`${dados.nome} aceitou seu desafio! 🎉`, {
        textoBotao: "Ir para o multiplayer",
        duracao: 15000,
        aoClicar: () => { window.location.href = dados.url_multiplayer; }
      });
    });
  });
})();
