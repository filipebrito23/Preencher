import time

import streamlit as st
from nba_api.live.nba.endpoints import boxscore


st.set_page_config(page_title="Teste de acesso à NBA")

st.title("Teste de acesso à NBA")
st.caption("Este teste apenas consulta dados. Não altera a planilha.")

game_id = st.text_input(
    "GameID",
    value="0022600204"
)

if st.button("Testar consulta"):
    game_id = game_id.strip()

    if len(game_id) != 10 or not game_id.isdigit():
        st.error("Informe um GameID com 10 dígitos.")
        st.stop()

    inicio = time.monotonic()

    try:
        with st.spinner("Consultando boxscore no CDN da NBA..."):
            resposta = boxscore.BoxScore(
                game_id=game_id,
                timeout=15,
                headers={
                    "Referer": "https://www.nba.com/",
                    "User-Agent": "Mozilla/5.0",
                },
            )

            dados = resposta.get_dict()

        duracao = time.monotonic() - inicio

        jogo = dados.get("game", {})
        mandante = jogo.get("homeTeam", {})
        visitante = jogo.get("awayTeam", {})

        jogadores = (
            mandante.get("players", [])
            + visitante.get("players", [])
        )

        st.success(f"Resposta recebida em {duracao:.1f} segundos.")

        st.write({
            "game_id": jogo.get("gameId"),
            "status": jogo.get("gameStatus"),
            "mandante": mandante.get("teamName"),
            "visitante": visitante.get("teamName"),
            "jogadores_retornados": len(jogadores),
        })

        with st.expander("Ver resposta completa"):
            st.json(dados)

    except Exception as exc:
        duracao = time.monotonic() - inicio

        st.error(f"Consulta falhou após {duracao:.1f} segundos.")
        st.code(
            f"{type(exc).__name__}: {exc}",
            language=None,
        )