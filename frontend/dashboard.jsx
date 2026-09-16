import { useState, useEffect, useRef } from "react";

// ── Dados mock de vagas (simulando feeds RSS + scraping) ──────────────────────
const MOCK_VAGAS = [
  {
    id: 1,
    titulo: "Estágio em Desenvolvimento de Software",
    empresa: "Stefanini",
    local: "Brasília, DF (Híbrido)",
    fonte: "Gupy",
    area: "Desenvolvimento",
    nivel: "Estágio",
    skills: ["Python", "SQL", "Git"],
    descricao: "Desenvolvimento de soluções internas, integração com APIs REST e suporte a sistemas legados.",
    url: "#",
    dataPublicacao: "2026-09-14",
    match: 92,
    nova: true,
  },
  {
    id: 2,
    titulo: "Estagiário TI – Suporte e Infraestrutura",
    empresa: "Banco do Brasil",
    local: "Brasília, DF (Presencial)",
    fonte: "CIEE",
    area: "Infraestrutura",
    nivel: "Estágio",
    skills: ["Windows Server", "Redes", "Active Directory"],
    descricao: "Suporte técnico a usuários internos, manutenção de equipamentos e gestão de chamados via GLPI.",
    url: "#",
    dataPublicacao: "2026-09-13",
    match: 74,
    nova: true,
  },
  {
    id: 3,
    titulo: "Estágio em Análise de Dados",
    empresa: "Serasa Experian",
    local: "Remoto",
    fonte: "Vagas.com.br",
    area: "Dados",
    nivel: "Estágio",
    skills: ["Power BI", "Excel", "SQL"],
    descricao: "Elaboração de dashboards para a equipe de risco, análise de indicadores e automatização de relatórios.",
    url: "#",
    dataPublicacao: "2026-09-13",
    match: 88,
    nova: false,
  },
  {
    id: 4,
    titulo: "Desenvolvedor Júnior – Backend",
    empresa: "Totvs",
    local: "Brasília, DF (Híbrido)",
    fonte: "LinkedIn RSS",
    area: "Desenvolvimento",
    nivel: "Júnior",
    skills: ["Java", "Spring Boot", "PostgreSQL"],
    descricao: "Desenvolvimento de módulos ERP, integração com sistemas de terceiros e testes unitários.",
    url: "#",
    dataPublicacao: "2026-09-12",
    match: 65,
    nova: false,
  },
  {
    id: 5,
    titulo: "Estágio em Segurança da Informação",
    empresa: "Serpro",
    local: "Brasília, DF (Presencial)",
    fonte: "Programathor",
    area: "Segurança",
    nivel: "Estágio",
    skills: ["Linux", "Redes", "Python"],
    descricao: "Monitoramento de incidentes, análise de logs e apoio na implementação de políticas de segurança.",
    url: "#",
    dataPublicacao: "2026-09-11",
    match: 71,
    nova: false,
  },
  {
    id: 6,
    titulo: "Estagiário – Desenvolvimento Web",
    empresa: "Accenture",
    local: "Brasília, DF (Híbrido)",
    fonte: "Gupy",
    area: "Desenvolvimento",
    nivel: "Estágio",
    skills: ["React", "JavaScript", "Node.js"],
    descricao: "Apoio na construção de interfaces web para clientes do setor público e financeiro.",
    url: "#",
    dataPublicacao: "2026-09-10",
    match: 83,
    nova: false,
  },
];

const FONTES = [
  { id: "gupy", nome: "Gupy", status: "ativo", icon: "◉" },
  { id: "ciee", nome: "CIEE", status: "ativo", icon: "◉" },
  { id: "vagas", nome: "Vagas.com.br", status: "ativo", icon: "◉" },
  { id: "programathor", nome: "Programathor", status: "ativo", icon: "◉" },
  { id: "linkedin", nome: "LinkedIn RSS", status: "ativo", icon: "◉" },
  { id: "indeed", nome: "Indeed", status: "limitado", icon: "◎" },
  { id: "glassdoor", nome: "Glassdoor", status: "bloqueado", icon: "○" },
];

const PERFIL = {
  nome: "Antonio Gabriel",
  area: "Desenvolvimento / TI",
  nivel: "Estágio",
  local: "Brasília, DF",
  skills: ["Python", "SQL", "Power BI", "Excel", "Git", "JavaScript"],
  curriculo: "Gestor de Finanças na Amoura Construtora + Auditor na Asoor Pro",
  certificacoes: ["AI-900 Azure", "Excel 2016", "Power BI", "BD Avançado"],
};

// ── Utilitários ───────────────────────────────────────────────────────────────
function matchColor(m) {
  if (m >= 85) return "#00D97E";
  if (m >= 70) return "#F5A623";
  return "#8899AA";
}

function matchLabel(m) {
  if (m >= 85) return "Ótimo fit";
  if (m >= 70) return "Bom fit";
  return "Fit parcial";
}

function fonteColor(status) {
  if (status === "ativo") return "#00D97E";
  if (status === "limitado") return "#F5A623";
  return "#556070";
}

function timeAgo(dateStr) {
  const d = new Date(dateStr);
  const now = new Date("2026-09-15");
  const diff = Math.floor((now - d) / 86400000);
  if (diff === 0) return "hoje";
  if (diff === 1) return "ontem";
  return `há ${diff} dias`;
}

// ── Componentes ───────────────────────────────────────────────────────────────

function Sidebar({ botAtivo, setBotAtivo, ultimaVerificacao, totalNovas, notifEmail, setNotifEmail }) {
  return (
    <aside style={{
      width: 240,
      minHeight: "100vh",
      background: "#0A1628",
      borderRight: "1px solid #1A2E4A",
      display: "flex",
      flexDirection: "column",
      padding: "28px 0",
      position: "fixed",
      top: 0,
      left: 0,
      zIndex: 10,
    }}>
      {/* Logo */}
      <div style={{ padding: "0 24px 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 32, height: 32,
            background: "linear-gradient(135deg, #00D97E, #0077FF)",
            borderRadius: 8,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 16,
          }}>⌖</div>
          <div>
            <div style={{ color: "#E8F0FA", fontSize: 14, fontWeight: 700, letterSpacing: -0.3 }}>VagaBot</div>
            <div style={{ color: "#4A6080", fontSize: 11 }}>monitor de vagas</div>
          </div>
        </div>
      </div>

      {/* Status do bot */}
      <div style={{ padding: "0 16px 24px" }}>
        <div style={{
          background: "#0F1E35",
          border: `1px solid ${botAtivo ? "#00D97E33" : "#1A2E4A"}`,
          borderRadius: 12,
          padding: "16px",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <span style={{ color: "#8899AA", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8 }}>Bot</span>
            <button
              onClick={() => setBotAtivo(!botAtivo)}
              style={{
                background: botAtivo ? "#00D97E22" : "#1A2E4A",
                border: `1px solid ${botAtivo ? "#00D97E" : "#2A3E5A"}`,
                borderRadius: 20,
                padding: "3px 12px",
                color: botAtivo ? "#00D97E" : "#556070",
                fontSize: 11,
                cursor: "pointer",
                fontWeight: 600,
                transition: "all 0.2s",
              }}
            >
              {botAtivo ? "ATIVO" : "PAUSADO"}
            </button>
          </div>
          <div style={{ color: "#4A6080", fontSize: 11, marginBottom: 4 }}>Última verificação</div>
          <div style={{ color: "#8899AA", fontSize: 12 }}>{ultimaVerificacao}</div>
          <div style={{ marginTop: 10, color: "#4A6080", fontSize: 11 }}>Próxima em</div>
          <div style={{ color: botAtivo ? "#00D97E" : "#556070", fontSize: 12, fontWeight: 600 }}>
            {botAtivo ? "~5 horas" : "—"}
          </div>
        </div>
      </div>

      {/* Notificações */}
      <div style={{ padding: "0 16px 24px" }}>
        <div style={{ color: "#4A6080", fontSize: 11, marginBottom: 10, paddingLeft: 4, textTransform: "uppercase", letterSpacing: 0.8 }}>Notificações</div>
        {[
          { id: "email", label: "Gmail", icon: "✉" },
          { id: "browser", label: "Navegador", icon: "🔔" },
        ].map(n => (
          <div key={n.id} style={{
            display: "flex", alignItems: "center", justifyContent: "space-between",
            padding: "8px 4px",
            borderBottom: "1px solid #1A2E4A",
          }}>
            <span style={{ color: "#8899AA", fontSize: 12 }}>{n.icon} {n.label}</span>
            <div
              onClick={() => n.id === "email" && setNotifEmail(!notifEmail)}
              style={{
                width: 32, height: 18,
                background: (n.id === "email" ? notifEmail : true) ? "#00D97E" : "#1A2E4A",
                borderRadius: 9,
                cursor: "pointer",
                position: "relative",
                transition: "background 0.2s",
              }}
            >
              <div style={{
                width: 14, height: 14,
                background: "#fff",
                borderRadius: "50%",
                position: "absolute",
                top: 2,
                left: (n.id === "email" ? notifEmail : true) ? 16 : 2,
                transition: "left 0.2s",
              }} />
            </div>
          </div>
        ))}
      </div>

      {/* Fontes */}
      <div style={{ padding: "0 16px", flex: 1 }}>
        <div style={{ color: "#4A6080", fontSize: 11, marginBottom: 10, paddingLeft: 4, textTransform: "uppercase", letterSpacing: 0.8 }}>Fontes</div>
        {FONTES.map(f => (
          <div key={f.id} style={{
            display: "flex", alignItems: "center", gap: 8,
            padding: "6px 4px",
          }}>
            <span style={{ color: fonteColor(f.status), fontSize: 10 }}>{f.icon}</span>
            <span style={{ color: f.status === "bloqueado" ? "#3A5060" : "#7A90A8", fontSize: 12 }}>{f.nome}</span>
            {f.status === "limitado" && (
              <span style={{ color: "#F5A623", fontSize: 9, marginLeft: "auto" }}>RSS</span>
            )}
            {f.status === "bloqueado" && (
              <span style={{ color: "#3A5060", fontSize: 9, marginLeft: "auto" }}>OFF</span>
            )}
          </div>
        ))}
      </div>

      {/* Rodapé */}
      <div style={{ padding: "24px 24px 0", borderTop: "1px solid #1A2E4A", marginTop: "auto" }}>
        <div style={{ color: "#3A5060", fontSize: 10 }}>github.com/antonio-gab</div>
      </div>
    </aside>
  );
}

function MatchBadge({ match }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 6,
    }}>
      <div style={{
        width: 36, height: 36,
        borderRadius: "50%",
        border: `2px solid ${matchColor(match)}`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 11, fontWeight: 700,
        color: matchColor(match),
        background: `${matchColor(match)}11`,
      }}>
        {match}
      </div>
      <div style={{ fontSize: 11, color: matchColor(match) }}>{matchLabel(match)}</div>
    </div>
  );
}

function VagaCard({ vaga, onVerDetalhe }) {
  return (
    <div
      onClick={() => onVerDetalhe(vaga)}
      style={{
        background: "#0F1E35",
        border: `1px solid ${vaga.nova ? "#00D97E33" : "#1A2E4A"}`,
        borderRadius: 14,
        padding: "20px 22px",
        cursor: "pointer",
        transition: "border-color 0.2s, transform 0.15s",
        position: "relative",
        overflow: "hidden",
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = "#00D97E66";
        e.currentTarget.style.transform = "translateY(-1px)";
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = vaga.nova ? "#00D97E33" : "#1A2E4A";
        e.currentTarget.style.transform = "translateY(0)";
      }}
    >
      {vaga.nova && (
        <div style={{
          position: "absolute", top: 16, right: 16,
          background: "#00D97E",
          color: "#000",
          fontSize: 9, fontWeight: 800,
          padding: "2px 8px",
          borderRadius: 20,
          letterSpacing: 0.8,
        }}>NOVA</div>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
        <div style={{ flex: 1, paddingRight: vaga.nova ? 48 : 0 }}>
          <div style={{ color: "#E8F0FA", fontSize: 15, fontWeight: 600, marginBottom: 4, lineHeight: 1.3 }}>
            {vaga.titulo}
          </div>
          <div style={{ color: "#4A8EC8", fontSize: 13, fontWeight: 500 }}>{vaga.empresa}</div>
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 14, flexWrap: "wrap" }}>
        <span style={{ color: "#6A80A0", fontSize: 12 }}>📍 {vaga.local}</span>
        <span style={{ color: "#6A80A0", fontSize: 12 }}>⏱ {timeAgo(vaga.dataPublicacao)}</span>
        <span style={{
          background: "#1A2E4A",
          color: "#8899AA",
          fontSize: 11, padding: "2px 8px", borderRadius: 6,
        }}>{vaga.fonte}</span>
      </div>

      <div style={{ display: "flex", gap: 6, marginBottom: 16, flexWrap: "wrap" }}>
        {vaga.skills.map(s => (
          <span key={s} style={{
            background: PERFIL.skills.includes(s) ? "#00D97E15" : "#1A2E4A",
            border: `1px solid ${PERFIL.skills.includes(s) ? "#00D97E44" : "#2A3E5A"}`,
            color: PERFIL.skills.includes(s) ? "#00D97E" : "#556070",
            fontSize: 11, padding: "2px 9px", borderRadius: 5,
          }}>{s}</span>
        ))}
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <MatchBadge match={vaga.match} />
        <span style={{ color: "#3A5070", fontSize: 12 }}>Ver detalhes →</span>
      </div>
    </div>
  );
}

function DetalheModal({ vaga, onClose }) {
  if (!vaga) return null;
  return (
    <div style={{
      position: "fixed", inset: 0,
      background: "#00000088",
      display: "flex", alignItems: "center", justifyContent: "center",
      zIndex: 100,
      padding: 24,
    }} onClick={onClose}>
      <div
        onClick={e => e.stopPropagation()}
        style={{
          background: "#0F1E35",
          border: "1px solid #1A3050",
          borderRadius: 18,
          padding: 32,
          maxWidth: 560,
          width: "100%",
          maxHeight: "80vh",
          overflowY: "auto",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20 }}>
          <div>
            <div style={{ color: "#E8F0FA", fontSize: 18, fontWeight: 700, marginBottom: 4 }}>{vaga.titulo}</div>
            <div style={{ color: "#4A8EC8", fontSize: 14 }}>{vaga.empresa}</div>
          </div>
          <button onClick={onClose} style={{
            background: "#1A2E4A", border: "none",
            color: "#8899AA", width: 32, height: 32,
            borderRadius: 8, cursor: "pointer", fontSize: 16,
          }}>✕</button>
        </div>

        <div style={{ display: "flex", gap: 16, marginBottom: 20, flexWrap: "wrap" }}>
          <span style={{ color: "#6A80A0", fontSize: 13 }}>📍 {vaga.local}</span>
          <span style={{ color: "#6A80A0", fontSize: 13 }}>🏢 {vaga.nivel}</span>
          <span style={{ color: "#6A80A0", fontSize: 13 }}>📂 {vaga.area}</span>
        </div>

        <div style={{ marginBottom: 20 }}>
          <MatchBadge match={vaga.match} />
        </div>

        <div style={{ marginBottom: 20 }}>
          <div style={{ color: "#4A6080", fontSize: 12, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.8 }}>Descrição</div>
          <div style={{ color: "#8899AA", fontSize: 14, lineHeight: 1.6 }}>{vaga.descricao}</div>
        </div>

        <div style={{ marginBottom: 24 }}>
          <div style={{ color: "#4A6080", fontSize: 12, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.8 }}>Skills exigidas</div>
          <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
            {vaga.skills.map(s => (
              <span key={s} style={{
                background: PERFIL.skills.includes(s) ? "#00D97E15" : "#1A2E4A",
                border: `1px solid ${PERFIL.skills.includes(s) ? "#00D97E44" : "#2A3E5A"}`,
                color: PERFIL.skills.includes(s) ? "#00D97E" : "#556070",
                fontSize: 12, padding: "4px 11px", borderRadius: 6,
              }}>
                {PERFIL.skills.includes(s) ? "✓ " : ""}{s}
              </span>
            ))}
          </div>
        </div>

        <a href={vaga.url} style={{
          display: "block",
          background: "linear-gradient(135deg, #00D97E, #0099FF)",
          color: "#000",
          textAlign: "center",
          padding: "14px",
          borderRadius: 10,
          fontWeight: 700,
          fontSize: 14,
          textDecoration: "none",
          letterSpacing: 0.3,
        }}>
          Abrir vaga em {vaga.fonte}
        </a>
      </div>
    </div>
  );
}

function NotifToast({ msg, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 4000);
    return () => clearTimeout(t);
  }, [onClose]);

  return (
    <div style={{
      position: "fixed", top: 24, right: 24,
      background: "#0F1E35",
      border: "1px solid #00D97E44",
      borderRadius: 12,
      padding: "14px 18px",
      display: "flex", alignItems: "center", gap: 12,
      zIndex: 200,
      maxWidth: 320,
      boxShadow: "0 8px 32px #00000060",
    }}>
      <div style={{ fontSize: 20 }}>🔔</div>
      <div>
        <div style={{ color: "#00D97E", fontSize: 12, fontWeight: 700, marginBottom: 2 }}>Nova vaga encontrada</div>
        <div style={{ color: "#8899AA", fontSize: 12 }}>{msg}</div>
      </div>
      <button onClick={onClose} style={{
        background: "none", border: "none",
        color: "#4A6080", cursor: "pointer", fontSize: 14, marginLeft: 4,
      }}>✕</button>
    </div>
  );
}

// ── App Principal ─────────────────────────────────────────────────────────────
export default function VagaBot() {
  const [botAtivo, setBotAtivo] = useState(true);
  const [notifEmail, setNotifEmail] = useState(true);
  const [vagaDetalhe, setVagaDetalhe] = useState(null);
  const [filtroArea, setFiltroArea] = useState("Todas");
  const [filtroMatch, setFiltroMatch] = useState(0);
  const [toast, setToast] = useState(null);
  const [abaAtiva, setAbaAtiva] = useState("vagas");
  const [buscandoAgora, setBuscandoAgora] = useState(false);
  const [vagas, setVagas] = useState(MOCK_VAGAS);
  const [emailConfig, setEmailConfig] = useState("antonio@gmail.com");
  const ultimaVerificacao = "hoje às 08:34";

  const areas = ["Todas", ...Array.from(new Set(MOCK_VAGAS.map(v => v.area)))];

  const vagasFiltradas = vagas
    .filter(v => filtroArea === "Todas" || v.area === filtroArea)
    .filter(v => v.match >= filtroMatch)
    .sort((a, b) => b.match - a.match);

  const totalNovas = vagas.filter(v => v.nova).length;

  function buscarAgora() {
    if (buscandoAgora) return;
    setBuscandoAgora(true);
    setTimeout(() => {
      setBuscandoAgora(false);
      const novaVaga = {
        id: 99,
        titulo: "Estágio em Cloud Computing – AWS",
        empresa: "Capgemini",
        local: "Brasília, DF (Remoto)",
        fonte: "Gupy",
        area: "Infraestrutura",
        nivel: "Estágio",
        skills: ["AWS", "Linux", "Python"],
        descricao: "Suporte a ambientes cloud, automação de tarefas e monitoramento de instâncias EC2.",
        url: "#",
        dataPublicacao: "2026-09-15",
        match: 79,
        nova: true,
      };
      setVagas(prev => [novaVaga, ...prev]);
      setToast("Estágio em Cloud Computing – Capgemini");
    }, 2800);
  }

  return (
    <div style={{
      fontFamily: "'Inter', system-ui, sans-serif",
      background: "#070E1C",
      minHeight: "100vh",
      color: "#E8F0FA",
      display: "flex",
    }}>
      <Sidebar
        botAtivo={botAtivo}
        setBotAtivo={setBotAtivo}
        ultimaVerificacao={ultimaVerificacao}
        totalNovas={totalNovas}
        notifEmail={notifEmail}
        setNotifEmail={setNotifEmail}
      />

      {/* Conteúdo principal */}
      <main style={{ marginLeft: 240, flex: 1, padding: "32px 36px", maxWidth: "calc(100vw - 240px)" }}>

        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 32 }}>
          <div>
            <div style={{ color: "#4A6080", fontSize: 13, marginBottom: 4 }}>Olá, Antonio Gabriel</div>
            <h1 style={{ color: "#E8F0FA", fontSize: 26, fontWeight: 700, margin: 0, letterSpacing: -0.5 }}>
              {totalNovas > 0
                ? <><span style={{ color: "#00D97E" }}>{totalNovas} novas vagas</span> encontradas</>
                : "Monitorando vagas"}
            </h1>
            <div style={{ color: "#4A6080", fontSize: 13, marginTop: 6 }}>
              {vagasFiltradas.length} vagas ativas · {FONTES.filter(f => f.status === "ativo").length} fontes ativas
            </div>
          </div>

          <button
            onClick={buscarAgora}
            disabled={buscandoAgora}
            style={{
              background: buscandoAgora ? "#1A2E4A" : "linear-gradient(135deg, #00D97E, #0077FF)",
              border: "none",
              color: buscandoAgora ? "#4A6080" : "#000",
              padding: "12px 22px",
              borderRadius: 10,
              fontWeight: 700,
              fontSize: 13,
              cursor: buscandoAgora ? "not-allowed" : "pointer",
              display: "flex", alignItems: "center", gap: 8,
              transition: "opacity 0.2s",
            }}
          >
            {buscandoAgora ? (
              <>⟳ Buscando...</>
            ) : (
              <>⌖ Buscar agora</>
            )}
          </button>
        </div>

        {/* Abas */}
        <div style={{ display: "flex", gap: 4, marginBottom: 28, borderBottom: "1px solid #1A2E4A", paddingBottom: 0 }}>
          {[
            { id: "vagas", label: `Vagas (${vagasFiltradas.length})` },
            { id: "perfil", label: "Meu Perfil" },
            { id: "config", label: "Configurações" },
          ].map(aba => (
            <button
              key={aba.id}
              onClick={() => setAbaAtiva(aba.id)}
              style={{
                background: "none",
                border: "none",
                borderBottom: `2px solid ${abaAtiva === aba.id ? "#00D97E" : "transparent"}`,
                color: abaAtiva === aba.id ? "#E8F0FA" : "#4A6080",
                padding: "8px 16px",
                cursor: "pointer",
                fontSize: 14,
                fontWeight: abaAtiva === aba.id ? 600 : 400,
                marginBottom: -1,
                transition: "color 0.15s",
              }}
            >
              {aba.label}
            </button>
          ))}
        </div>

        {/* Aba: Vagas */}
        {abaAtiva === "vagas" && (
          <>
            {/* Filtros */}
            <div style={{ display: "flex", gap: 12, marginBottom: 24, flexWrap: "wrap", alignItems: "center" }}>
              <div style={{ display: "flex", gap: 6 }}>
                {areas.map(a => (
                  <button
                    key={a}
                    onClick={() => setFiltroArea(a)}
                    style={{
                      background: filtroArea === a ? "#00D97E22" : "#0F1E35",
                      border: `1px solid ${filtroArea === a ? "#00D97E" : "#1A2E4A"}`,
                      color: filtroArea === a ? "#00D97E" : "#6A80A0",
                      padding: "6px 14px",
                      borderRadius: 8,
                      fontSize: 12,
                      cursor: "pointer",
                      fontWeight: filtroArea === a ? 600 : 400,
                    }}
                  >{a}</button>
                ))}
              </div>

              <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ color: "#4A6080", fontSize: 12 }}>Match mín.</span>
                <input
                  type="range" min={0} max={85} step={5}
                  value={filtroMatch}
                  onChange={e => setFiltroMatch(+e.target.value)}
                  style={{ accentColor: "#00D97E", width: 80 }}
                />
                <span style={{ color: "#00D97E", fontSize: 12, fontWeight: 700, width: 28 }}>{filtroMatch}%</span>
              </div>
            </div>

            {/* Grid de vagas */}
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(360px, 1fr))",
              gap: 16,
            }}>
              {vagasFiltradas.map(v => (
                <VagaCard key={v.id} vaga={v} onVerDetalhe={setVagaDetalhe} />
              ))}
              {vagasFiltradas.length === 0 && (
                <div style={{ color: "#3A5060", gridColumn: "1/-1", textAlign: "center", padding: 40 }}>
                  Nenhuma vaga com esses filtros.
                </div>
              )}
            </div>
          </>
        )}

        {/* Aba: Perfil */}
        {abaAtiva === "perfil" && (
          <div style={{ maxWidth: 600 }}>
            <div style={{
              background: "#0F1E35", border: "1px solid #1A2E4A",
              borderRadius: 16, padding: 28, marginBottom: 20,
            }}>
              <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 16 }}>Perfil detectado pelo bot</div>

              {[
                { label: "Nome", val: PERFIL.nome },
                { label: "Área-alvo", val: PERFIL.area },
                { label: "Nível", val: PERFIL.nivel },
                { label: "Localização", val: PERFIL.local },
                { label: "Experiência", val: PERFIL.curriculo },
              ].map(r => (
                <div key={r.label} style={{ display: "flex", gap: 16, padding: "10px 0", borderBottom: "1px solid #1A2E4A" }}>
                  <div style={{ color: "#4A6080", fontSize: 13, width: 110, flexShrink: 0 }}>{r.label}</div>
                  <div style={{ color: "#C8D8E8", fontSize: 13 }}>{r.val}</div>
                </div>
              ))}

              <div style={{ display: "flex", gap: 16, padding: "10px 0", borderBottom: "1px solid #1A2E4A" }}>
                <div style={{ color: "#4A6080", fontSize: 13, width: 110, flexShrink: 0 }}>Skills</div>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  {PERFIL.skills.map(s => (
                    <span key={s} style={{
                      background: "#00D97E15", border: "1px solid #00D97E44",
                      color: "#00D97E", fontSize: 12, padding: "2px 9px", borderRadius: 5,
                    }}>{s}</span>
                  ))}
                </div>
              </div>

              <div style={{ display: "flex", gap: 16, padding: "10px 0" }}>
                <div style={{ color: "#4A6080", fontSize: 13, width: 110, flexShrink: 0 }}>Certificações</div>
                <div style={{ color: "#C8D8E8", fontSize: 13, lineHeight: 1.8 }}>
                  {PERFIL.certificacoes.join(" · ")}
                </div>
              </div>
            </div>

            <div style={{ color: "#4A6080", fontSize: 13, lineHeight: 1.6, padding: "0 4px" }}>
              💡 O bot usa essas informações para calcular o <span style={{ color: "#00D97E" }}>score de match</span> de cada vaga.
              Skills que aparecem em verde nas vagas são as que você já tem no perfil.
            </div>
          </div>
        )}

        {/* Aba: Configurações */}
        {abaAtiva === "config" && (
          <div style={{ maxWidth: 560 }}>
            <div style={{
              background: "#0F1E35", border: "1px solid #1A2E4A",
              borderRadius: 16, padding: 28, marginBottom: 20,
            }}>
              <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 20 }}>Notificação por e-mail</div>

              <label style={{ color: "#8899AA", fontSize: 13, display: "block", marginBottom: 8 }}>Endereço Gmail</label>
              <input
                value={emailConfig}
                onChange={e => setEmailConfig(e.target.value)}
                style={{
                  background: "#0A1628", border: "1px solid #1A3050",
                  color: "#E8F0FA", padding: "10px 14px",
                  borderRadius: 8, fontSize: 13,
                  width: "100%", boxSizing: "border-box", marginBottom: 16,
                  outline: "none",
                }}
              />

              <label style={{ color: "#8899AA", fontSize: 13, display: "block", marginBottom: 8 }}>Frequência de verificação</label>
              <select style={{
                background: "#0A1628", border: "1px solid #1A3050",
                color: "#E8F0FA", padding: "10px 14px",
                borderRadius: 8, fontSize: 13,
                width: "100%", boxSizing: "border-box", marginBottom: 20,
                outline: "none",
              }}>
                <option>A cada 6 horas</option>
                <option>A cada 12 horas</option>
                <option>Uma vez ao dia</option>
              </select>

              <label style={{ color: "#8899AA", fontSize: 13, display: "block", marginBottom: 8 }}>Match mínimo para notificar</label>
              <select style={{
                background: "#0A1628", border: "1px solid #1A3050",
                color: "#E8F0FA", padding: "10px 14px",
                borderRadius: 8, fontSize: 13,
                width: "100%", boxSizing: "border-box",
                outline: "none",
              }}>
                <option>70% ou mais</option>
                <option>80% ou mais</option>
                <option>Todas as vagas</option>
              </select>
            </div>

            <div style={{
              background: "#0F1E35", border: "1px solid #1A2E4A",
              borderRadius: 16, padding: 28,
            }}>
              <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 16 }}>Palavras-chave extras</div>
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 12 }}>
                {["estágio", "Brasília", "Python", "banco de dados", "TI"].map(k => (
                  <span key={k} style={{
                    background: "#1A2E4A", border: "1px solid #2A3E5A",
                    color: "#8899AA", fontSize: 12, padding: "4px 11px", borderRadius: 6,
                  }}>{k} ✕</span>
                ))}
              </div>
              <div style={{ color: "#3A5060", fontSize: 12 }}>+ Adicionar palavra-chave</div>
            </div>
          </div>
        )}
      </main>

      {/* Modal de detalhe */}
      <DetalheModal vaga={vagaDetalhe} onClose={() => setVagaDetalhe(null)} />

      {/* Toast de notificação */}
      {toast && <NotifToast msg={toast} onClose={() => setToast(null)} />}
    </div>
  );
}
