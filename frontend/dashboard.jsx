const { useState, useEffect, useCallback } = React;

// ── Perfil (espelho do config.py — skills usadas para colorir os cards) ───────
const PERFIL_SKILLS = ["Python", "SQL", "Power BI", "Excel", "Git", "JavaScript"];

// ── Fontes com status real do projeto ────────────────────────────────────────
const FONTES = [
  { nome: "GitHub/frontendbr", status: "ativo"    },
  { nome: "GitHub/backend-br", status: "ativo"    },
  { nome: "Gupy (RSS)",        status: "inativo"  },
  { nome: "Vagas.com.br",      status: "inativo"  },
  { nome: "Programathor",      status: "inativo"  },
  { nome: "CIEE",              status: "pendente" },
  { nome: "LinkedIn RSS",      status: "pendente" },
];

// ── Utilitários ───────────────────────────────────────────────────────────────
function matchCor(m)   { return m >= 85 ? "#00D97E" : m >= 70 ? "#F5A623" : "#8899AA"; }
function matchLabel(m) { return m >= 85 ? "Ótimo fit" : m >= 70 ? "Bom fit" : "Fit parcial"; }

function timeAgo(str) {
  if (!str) return "—";
  const diff = Math.floor((Date.now() - new Date(str)) / 86400000);
  if (diff === 0) return "hoje";
  if (diff === 1) return "ontem";
  if (diff < 0)  return "recente";
  return `há ${diff} dias`;
}

function statusCor(s) {
  return s === "ativo" ? "#00D97E" : s === "inativo" ? "#4A6080" : "#F5A623";
}
function statusLabel(s) {
  return s === "ativo" ? "●" : s === "inativo" ? "○" : "◎";
}

// ── Estado de carregamento ────────────────────────────────────────────────────
function Loading() {
  return (
    <div style={{ gridColumn: "1/-1", textAlign: "center", padding: "60px 0", color: "#4A6080" }}>
      <div style={{ fontSize: 32, marginBottom: 12 }}>⟳</div>
      <div style={{ fontSize: 14 }}>Buscando vagas reais…</div>
    </div>
  );
}

function Vazio({ erro }) {
  return (
    <div style={{ gridColumn: "1/-1", textAlign: "center", padding: "60px 0" }}>
      {erro
        ? <div style={{ color: "#FF6B6B", fontSize: 14, maxWidth: 420, margin: "0 auto", lineHeight: 1.6 }}>
            <div style={{ fontSize: 28, marginBottom: 12 }}>⚠️</div>
            {erro}
            <div style={{ marginTop: 12, fontSize: 12, color: "#4A6080" }}>
              Verifique se o backend está rodando com <code>python backend/app.py</code>
            </div>
          </div>
        : <div style={{ color: "#4A6080", fontSize: 14 }}>
            <div style={{ fontSize: 28, marginBottom: 12 }}>🔍</div>
            Nenhuma vaga encontrada com esses filtros.
          </div>
      }
    </div>
  );
}

// ── Sidebar ───────────────────────────────────────────────────────────────────
function Sidebar({ ultimaVerif, totalNovas, carregando }) {
  return (
    <aside style={{
      width: 230, minHeight: "100vh", background: "#0A1628",
      borderRight: "1px solid #1A2E4A", display: "flex",
      flexDirection: "column", padding: "24px 0", position: "fixed",
      top: 0, left: 0, zIndex: 10,
    }}>
      {/* Logo */}
      <div style={{ padding: "0 20px 24px", borderBottom: "1px solid #1A2E4A" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 10, fontSize: 18,
            background: "linear-gradient(135deg,#00D97E,#0077FF)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>🤖</div>
          <div>
            <div style={{ color: "#E8F0FA", fontSize: 15, fontWeight: 700 }}>VagaBot</div>
            <div style={{ color: "#4A6080", fontSize: 11 }}>monitor de vagas</div>
          </div>
        </div>
      </div>

      {/* Status */}
      <div style={{ padding: "16px 16px 0" }}>
        <div style={{
          background: "#0F1E35", border: "1px solid #1A2E4A",
          borderRadius: 12, padding: 14,
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
            <span style={{ color: "#8899AA", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8 }}>Status</span>
            <span style={{
              background: "#00D97E22", border: "1px solid #00D97E",
              color: "#00D97E", fontSize: 10, fontWeight: 700,
              padding: "2px 8px", borderRadius: 20,
            }}>ATIVO</span>
          </div>
          <div style={{ color: "#4A6080", fontSize: 11, marginBottom: 2 }}>Última busca</div>
          <div style={{ color: "#8899AA", fontSize: 11 }}>{ultimaVerif || "—"}</div>
          {totalNovas > 0 && (
            <div style={{ marginTop: 10, color: "#00D97E", fontSize: 12, fontWeight: 600 }}>
              {totalNovas} nova{totalNovas > 1 ? "s" : ""} vaga{totalNovas > 1 ? "s" : ""}
            </div>
          )}
        </div>
      </div>

      {/* Fontes */}
      <div style={{ padding: "20px 16px 0", flex: 1 }}>
        <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 10, paddingLeft: 4 }}>
          Fontes
        </div>
        {FONTES.map(f => (
          <div key={f.nome} style={{ display: "flex", alignItems: "center", gap: 8, padding: "5px 4px" }}>
            <span style={{ color: statusCor(f.status), fontSize: 10 }}>{statusLabel(f.status)}</span>
            <span style={{ color: f.status === "ativo" ? "#8899AA" : "#3A5060", fontSize: 12 }}>{f.nome}</span>
          </div>
        ))}
        <div style={{ marginTop: 10, paddingLeft: 4, fontSize: 10, color: "#2A3E5A", lineHeight: 1.6 }}>
          ● ativo &nbsp; ◎ em breve &nbsp; ○ inativo
        </div>
      </div>

      {/* Rodapé */}
      <div style={{ padding: "16px 20px 0", borderTop: "1px solid #1A2E4A" }}>
        <a href="https://github.com/antonio-gab/vagabot" target="_blank"
          style={{ color: "#3A5060", fontSize: 10, textDecoration: "none" }}>
          github.com/antonio-gab/vagabot
        </a>
      </div>
    </aside>
  );
}

// ── Card de vaga ──────────────────────────────────────────────────────────────
function VagaCard({ vaga, onClick }) {
  const skills = vaga.skills_match || [];
  const skillsFaltando = vaga.skills_faltando || [];
  const todasSkills = [...new Set([...skills, ...skillsFaltando])];

  return (
    <div
      onClick={() => onClick(vaga)}
      style={{
        background: "#0F1E35",
        border: `1px solid ${vaga.nova ? "#00D97E44" : "#1A2E4A"}`,
        borderRadius: 14, padding: "18px 20px",
        cursor: "pointer", position: "relative",
        transition: "border-color 0.15s, transform 0.1s",
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = "#00D97E88";
        e.currentTarget.style.transform = "translateY(-2px)";
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = vaga.nova ? "#00D97E44" : "#1A2E4A";
        e.currentTarget.style.transform = "translateY(0)";
      }}
    >
      {vaga.nova && (
        <div style={{
          position: "absolute", top: 14, right: 14,
          background: "#00D97E", color: "#000",
          fontSize: 9, fontWeight: 800, padding: "2px 7px",
          borderRadius: 20, letterSpacing: 0.8,
        }}>NOVA</div>
      )}

      {/* Título e empresa */}
      <div style={{ color: "#E8F0FA", fontSize: 14, fontWeight: 600, lineHeight: 1.4, marginBottom: 3, paddingRight: vaga.nova ? 50 : 0 }}>
        {vaga.titulo}
      </div>
      <div style={{ color: "#4A8EC8", fontSize: 12, marginBottom: 10 }}>
        {vaga.empresa || vaga.fonte}
      </div>

      {/* Meta */}
      <div style={{ display: "flex", gap: 10, marginBottom: 12, flexWrap: "wrap" }}>
        <span style={{ color: "#6A80A0", fontSize: 11 }}>📍 {vaga.local || "Não informado"}</span>
        <span style={{ color: "#6A80A0", fontSize: 11 }}>⏱ {timeAgo(vaga.data)}</span>
        <span style={{ background: "#1A2E4A", color: "#6A80A0", fontSize: 10, padding: "1px 7px", borderRadius: 5 }}>
          {vaga.fonte}
        </span>
      </div>

      {/* Skills */}
      {todasSkills.length > 0 && (
        <div style={{ display: "flex", gap: 5, marginBottom: 14, flexWrap: "wrap" }}>
          {todasSkills.slice(0, 6).map(s => {
            const tenho = skills.includes(s);
            return (
              <span key={s} style={{
                background: tenho ? "#00D97E15" : "#1A2E4A",
                border: `1px solid ${tenho ? "#00D97E44" : "#2A3E5A"}`,
                color: tenho ? "#00D97E" : "#556070",
                fontSize: 10, padding: "2px 8px", borderRadius: 5,
              }}>{tenho ? "✓ " : ""}{s}</span>
            );
          })}
        </div>
      )}

      {/* Match */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{
            width: 34, height: 34, borderRadius: "50%",
            border: `2px solid ${matchCor(vaga.match)}`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 11, fontWeight: 700, color: matchCor(vaga.match),
            background: `${matchCor(vaga.match)}11`,
          }}>{vaga.match}%</div>
          <span style={{ fontSize: 11, color: matchCor(vaga.match) }}>{matchLabel(vaga.match)}</span>
        </div>
        <span style={{ color: "#3A5070", fontSize: 11 }}>Ver detalhes →</span>
      </div>
    </div>
  );
}

// ── Modal de detalhe ──────────────────────────────────────────────────────────
function Modal({ vaga, onClose }) {
  if (!vaga) return null;
  const skills = vaga.skills_match || [];
  const skillsFaltando = vaga.skills_faltando || [];
  const todasSkills = [...new Set([...skills, ...skillsFaltando])];

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed", inset: 0, background: "#000000aa",
        display: "flex", alignItems: "center", justifyContent: "center",
        zIndex: 100, padding: 24,
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          background: "#0F1E35", border: "1px solid #1A3050",
          borderRadius: 18, padding: 28, maxWidth: 560,
          width: "100%", maxHeight: "85vh", overflowY: "auto",
        }}
      >
        {/* Cabeçalho */}
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <div style={{ flex: 1, paddingRight: 12 }}>
            <div style={{ color: "#E8F0FA", fontSize: 17, fontWeight: 700, lineHeight: 1.4, marginBottom: 4 }}>
              {vaga.titulo}
            </div>
            <div style={{ color: "#4A8EC8", fontSize: 13 }}>{vaga.empresa || vaga.fonte}</div>
          </div>
          <button onClick={onClose} style={{
            background: "#1A2E4A", border: "none", color: "#8899AA",
            width: 30, height: 30, borderRadius: 8, cursor: "pointer", fontSize: 15, flexShrink: 0,
          }}>✕</button>
        </div>

        {/* Meta */}
        <div style={{ display: "flex", gap: 14, flexWrap: "wrap", padding: "12px 0", borderTop: "1px solid #1A2E4A", borderBottom: "1px solid #1A2E4A", marginBottom: 16 }}>
          <span style={{ color: "#6A80A0", fontSize: 12 }}>📍 {vaga.local || "Não informado"}</span>
          <span style={{ color: "#6A80A0", fontSize: 12 }}>🏷 {vaga.nivel || "—"}</span>
          <span style={{ color: "#6A80A0", fontSize: 12 }}>📂 {vaga.area || "—"}</span>
          <span style={{ color: "#6A80A0", fontSize: 12 }}>📅 {timeAgo(vaga.data)}</span>
          <span style={{ color: "#6A80A0", fontSize: 12 }}>🔗 {vaga.fonte}</span>
        </div>

        {/* Match */}
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 18 }}>
          <div style={{
            width: 40, height: 40, borderRadius: "50%",
            border: `2px solid ${matchCor(vaga.match)}`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 12, fontWeight: 700, color: matchCor(vaga.match),
            background: `${matchCor(vaga.match)}11`, flexShrink: 0,
          }}>{vaga.match}%</div>
          <span style={{ color: matchCor(vaga.match), fontSize: 13 }}>
            {matchLabel(vaga.match)} — {skills.length} de {todasSkills.length} skills no seu perfil
          </span>
        </div>

        {/* Labels */}
        {vaga.labels && vaga.labels.length > 0 && (
          <div style={{ marginBottom: 16 }}>
            <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 8 }}>Labels</div>
            <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
              {vaga.labels.map(l => (
                <span key={l} style={{
                  background: "#1A2E4A", color: "#8899AA",
                  fontSize: 11, padding: "3px 9px", borderRadius: 6,
                }}>{l}</span>
              ))}
            </div>
          </div>
        )}

        {/* Skills */}
        {todasSkills.length > 0 && (
          <div style={{ marginBottom: 16 }}>
            <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 8 }}>Skills</div>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
              {todasSkills.map(s => {
                const tenho = skills.includes(s);
                return (
                  <span key={s} style={{
                    background: tenho ? "#00D97E15" : "#1A2E4A",
                    border: `1px solid ${tenho ? "#00D97E44" : "#2A3E5A"}`,
                    color: tenho ? "#00D97E" : "#556070",
                    fontSize: 12, padding: "3px 10px", borderRadius: 6,
                  }}>{tenho ? "✓ " : ""}{s}</span>
                );
              })}
            </div>
          </div>
        )}

        {/* Descrição */}
        {vaga.descricao && (
          <div style={{ marginBottom: 20 }}>
            <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 8 }}>Descrição</div>
            <div style={{
              color: "#8899AA", fontSize: 13, lineHeight: 1.7,
              maxHeight: 180, overflowY: "auto",
              background: "#0A1628", borderRadius: 8, padding: 12,
              whiteSpace: "pre-wrap",
            }}>
              {vaga.descricao}
            </div>
          </div>
        )}

        {/* CTA */}
        <a
          href={vaga.url} target="_blank" rel="noopener noreferrer"
          style={{
            display: "block", background: "linear-gradient(135deg,#00D97E,#0077FF)",
            color: "#000", textAlign: "center", padding: 13, borderRadius: 10,
            fontWeight: 700, fontSize: 14, textDecoration: "none",
          }}
        >
          Abrir vaga →
        </a>
      </div>
    </div>
  );
}

// ── Toast ────────────────────────────────────────────────────────────────────
function Toast({ msg, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 4000);
    return () => clearTimeout(t);
  }, [onClose]);

  return (
    <div style={{
      position: "fixed", bottom: 24, right: 24,
      background: "#0F1E35", border: "1px solid #00D97E44",
      borderRadius: 12, padding: "12px 16px",
      display: "flex", alignItems: "center", gap: 10,
      zIndex: 200, maxWidth: 300, boxShadow: "0 8px 32px #00000060",
    }}>
      <span style={{ fontSize: 18 }}>🔔</span>
      <div style={{ flex: 1 }}>
        <div style={{ color: "#00D97E", fontSize: 11, fontWeight: 700, marginBottom: 2 }}>VagaBot</div>
        <div style={{ color: "#8899AA", fontSize: 12 }}>{msg}</div>
      </div>
      <button onClick={onClose} style={{ background: "none", border: "none", color: "#4A6080", cursor: "pointer", fontSize: 14 }}>✕</button>
    </div>
  );
}

// ── App ───────────────────────────────────────────────────────────────────────
function VagaBot() {
  const [vagas, setVagas]               = useState([]);
  const [carregando, setCarregando]     = useState(false);
  const [erro, setErro]                 = useState(null);
  const [ultimaVerif, setUltimaVerif]   = useState(null);
  const [totalNovas, setTotalNovas]     = useState(0);
  const [modalVaga, setModalVaga]       = useState(null);
  const [toast, setToast]               = useState(null);
  const [filtroArea, setFiltroArea]     = useState("Todas");
  const [filtroMatch, setFiltroMatch]   = useState(0);
  const [abaAtiva, setAbaAtiva]         = useState("vagas");

  // Carrega vagas já em cache do servidor (sem re-buscar)
  const carregarCached = useCallback(async () => {
    try {
      const r = await fetch("/api/vagas");
      if (!r.ok) return;
      const d = await r.json();
      if (d.vagas && d.vagas.length) {
        setVagas(d.vagas);
        setTotalNovas(d.total_novas || 0);
        setUltimaVerif(d.atualizado_em ? new Date(d.atualizado_em).toLocaleString("pt-BR") : null);
      }
    } catch (_) {}
  }, []);

  // Dispara nova busca no backend
  const buscarAgora = useCallback(async () => {
    if (carregando) return;
    setCarregando(true);
    setErro(null);
    try {
      const r = await fetch("/api/buscar", { method: "POST" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const d = await r.json();
      if (d.erro) throw new Error(d.erro);
      setVagas(d.vagas || []);
      setTotalNovas(d.total_novas || 0);
      setUltimaVerif(d.atualizado_em ? new Date(d.atualizado_em).toLocaleString("pt-BR") : null);
      setToast(`${(d.vagas || []).length} vaga(s) carregada(s) com dados reais.`);
    } catch (e) {
      setErro("Não foi possível conectar ao backend. Certifique-se de que o servidor está rodando com: python backend/app.py");
    } finally {
      setCarregando(false);
    }
  }, [carregando]);

  // Ao abrir: tenta cache, depois busca
  useEffect(() => {
    carregarCached().then(buscarAgora);
  }, []);

  // Áreas disponíveis nas vagas carregadas
  const areas = ["Todas", ...Array.from(new Set(vagas.map(v => v.area).filter(Boolean)))];

  const vagasFiltradas = vagas
    .filter(v => filtroArea === "Todas" || v.area === filtroArea)
    .filter(v => (v.match || 0) >= filtroMatch)
    .sort((a, b) => (b.match || 0) - (a.match || 0));

  return (
    <div style={{
      fontFamily: "'Inter', system-ui, sans-serif",
      background: "#070E1C", minHeight: "100vh",
      color: "#E8F0FA", display: "flex",
    }}>
      <Sidebar ultimaVerif={ultimaVerif} totalNovas={totalNovas} carregando={carregando} />

      <main style={{ marginLeft: 230, flex: 1, padding: "28px 32px" }}>

        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28 }}>
          <div>
            <div style={{ color: "#4A6080", fontSize: 13, marginBottom: 4 }}>Olá, Antonio Gabriel</div>
            <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700, letterSpacing: -0.5 }}>
              {totalNovas > 0
                ? <><span style={{ color: "#00D97E" }}>{totalNovas} nova{totalNovas > 1 ? "s" : ""}</span> vaga{totalNovas > 1 ? "s" : ""} encontrada{totalNovas > 1 ? "s" : ""}</>
                : "Monitorando vagas"
              }
            </h1>
            <div style={{ color: "#4A6080", fontSize: 13, marginTop: 5 }}>
              {vagas.length} vaga{vagas.length !== 1 ? "s" : ""} coletada{vagas.length !== 1 ? "s" : ""} · {FONTES.filter(f => f.status === "ativo").length} fontes ativas
            </div>
          </div>

          <button
            onClick={buscarAgora}
            disabled={carregando}
            style={{
              background: carregando ? "#1A2E4A" : "linear-gradient(135deg,#00D97E,#0077FF)",
              border: "none", color: carregando ? "#4A6080" : "#000",
              padding: "11px 20px", borderRadius: 10,
              fontWeight: 700, fontSize: 13, cursor: carregando ? "not-allowed" : "pointer",
              display: "flex", alignItems: "center", gap: 7,
              transition: "opacity 0.2s",
            }}
          >
            {carregando ? "⟳ Buscando…" : "⌖ Buscar agora"}
          </button>
        </div>

        {/* Abas */}
        <div style={{ display: "flex", gap: 2, marginBottom: 24, borderBottom: "1px solid #1A2E4A" }}>
          {[
            { id: "vagas",  label: `Vagas (${vagasFiltradas.length})` },
            { id: "perfil", label: "Meu perfil" },
          ].map(aba => (
            <button key={aba.id} onClick={() => setAbaAtiva(aba.id)} style={{
              background: "none", border: "none",
              borderBottom: `2px solid ${abaAtiva === aba.id ? "#00D97E" : "transparent"}`,
              color: abaAtiva === aba.id ? "#E8F0FA" : "#4A6080",
              padding: "8px 16px", cursor: "pointer", fontSize: 14,
              fontWeight: abaAtiva === aba.id ? 600 : 400,
              marginBottom: -1, transition: "color 0.15s",
            }}>{aba.label}</button>
          ))}
        </div>

        {/* Aba Vagas */}
        {abaAtiva === "vagas" && (
          <>
            {/* Filtros */}
            <div style={{ display: "flex", gap: 8, marginBottom: 20, flexWrap: "wrap", alignItems: "center" }}>
              {areas.map(a => (
                <button key={a} onClick={() => setFiltroArea(a)} style={{
                  background: filtroArea === a ? "#00D97E22" : "#0F1E35",
                  border: `1px solid ${filtroArea === a ? "#00D97E" : "#1A2E4A"}`,
                  color: filtroArea === a ? "#00D97E" : "#6A80A0",
                  padding: "5px 13px", borderRadius: 20, fontSize: 12,
                  cursor: "pointer", fontWeight: filtroArea === a ? 600 : 400,
                  transition: "all 0.1s",
                }}>{a}</button>
              ))}
              <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ color: "#4A6080", fontSize: 12 }}>Match mín.</span>
                <input
                  type="range" min={0} max={80} step={5} value={filtroMatch}
                  onChange={e => setFiltroMatch(+e.target.value)}
                  style={{ accentColor: "#00D97E", width: 80 }}
                />
                <span style={{ color: "#00D97E", fontSize: 12, fontWeight: 700, minWidth: 28 }}>{filtroMatch}%</span>
              </div>
            </div>

            {/* Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(340px,1fr))", gap: 14 }}>
              {carregando
                ? <Loading />
                : erro
                  ? <Vazio erro={erro} />
                  : vagasFiltradas.length === 0
                    ? <Vazio />
                    : vagasFiltradas.map(v => (
                        <VagaCard key={v.id || v.url} vaga={v} onClick={setModalVaga} />
                      ))
              }
            </div>
          </>
        )}

        {/* Aba Perfil */}
        {abaAtiva === "perfil" && (
          <div style={{ maxWidth: 560 }}>
            <div style={{
              background: "#0F1E35", border: "1px solid #1A2E4A",
              borderRadius: 14, padding: 24, marginBottom: 16,
            }}>
              <div style={{ color: "#4A6080", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 16 }}>
                Perfil ativo no bot
              </div>
              {[
                ["Nome",        "Antonio Gabriel Vieira Paiva"],
                ["Área alvo",   "Desenvolvimento / TI"],
                ["Nível",       "Estágio"],
                ["Localização", "Brasília, DF"],
                ["Experiência", "Gestor de Finanças (Amoura) · Auditor (Asoor Pro)"],
                ["Certificações", "AI-900 Azure · Excel 2016 · Power BI · Banco de Dados"],
              ].map(([k, v]) => (
                <div key={k} style={{ display: "flex", gap: 14, padding: "9px 0", borderBottom: "1px solid #1A2E4A" }}>
                  <div style={{ color: "#4A6080", fontSize: 13, width: 110, flexShrink: 0 }}>{k}</div>
                  <div style={{ color: "#C8D8E8", fontSize: 13 }}>{v}</div>
                </div>
              ))}
              <div style={{ display: "flex", gap: 14, padding: "9px 0" }}>
                <div style={{ color: "#4A6080", fontSize: 13, width: 110, flexShrink: 0 }}>Skills</div>
                <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
                  {PERFIL_SKILLS.map(s => (
                    <span key={s} style={{
                      background: "#00D97E15", border: "1px solid #00D97E44",
                      color: "#00D97E", fontSize: 12, padding: "2px 9px", borderRadius: 5,
                    }}>{s}</span>
                  ))}
                </div>
              </div>
            </div>
            <div style={{
              background: "#0F1E1A", border: "1px solid #00D97E22",
              borderRadius: 10, padding: "12px 14px",
              color: "#4A8060", fontSize: 13, lineHeight: 1.6,
            }}>
              💡 Skills em <span style={{ color: "#00D97E" }}>verde</span> nos cards são as que você já tem.
              As em cinza são gaps — uma dica do que estudar para aumentar o match.
            </div>
          </div>
        )}
      </main>

      <Modal vaga={modalVaga} onClose={() => setModalVaga(null)} />
      {toast && <Toast msg={toast} onClose={() => setToast(null)} />}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<VagaBot />);
