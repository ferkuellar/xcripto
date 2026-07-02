// Series de métricas ficticias para las gráficas del dashboard.

export const productionByDay = [
  { day: 'Lun', drafted: 8, published: 5 },
  { day: 'Mar', drafted: 11, published: 7 },
  { day: 'Mié', drafted: 9, published: 8 },
  { day: 'Jue', drafted: 13, published: 9 },
  { day: 'Vie', drafted: 15, published: 11 },
  { day: 'Sáb', drafted: 6, published: 6 },
  { day: 'Dom', drafted: 5, published: 4 },
]

export const publicationsByChannel = [
  { channel: 'Blog / Web', count: 14 },
  { channel: 'X / Twitter', count: 22 },
  { channel: 'YouTube', count: 6 },
  { channel: 'Shorts', count: 12 },
  { channel: 'Newsletter', count: 4 },
  { channel: 'LinkedIn', count: 8 },
  { channel: 'Telegram', count: 10 },
]

export const risksByCategory = [
  { category: 'Regulación', critical: 0, high: 2, medium: 4, low: 6 },
  { category: 'Mercados', critical: 1, high: 3, medium: 5, low: 4 },
  { category: 'Seguridad', critical: 2, high: 2, medium: 1, low: 2 },
  { category: 'Tecnología', critical: 0, high: 1, medium: 3, low: 7 },
  { category: 'Institucional', critical: 0, high: 0, medium: 2, low: 5 },
]

export const agentRunsByDay = [
  { day: 'Lun', runs: 96 },
  { day: 'Mar', runs: 112 },
  { day: 'Mié', runs: 104 },
  { day: 'Jue', runs: 128 },
  { day: 'Vie', runs: 141 },
  { day: 'Sáb', runs: 87 },
  { day: 'Dom', runs: 74 },
]

export const verificationTime = [
  { day: 'Lun', minutes: 42 },
  { day: 'Mar', minutes: 38 },
  { day: 'Mié', minutes: 45 },
  { day: 'Jue', minutes: 33 },
  { day: 'Vie', minutes: 29 },
  { day: 'Sáb', minutes: 31 },
  { day: 'Dom', minutes: 27 },
]

export const engagementByChannel = [
  { channel: 'YouTube', engagement: 6.8 },
  { channel: 'Shorts', engagement: 9.2 },
  { channel: 'TikTok', engagement: 11.4 },
  { channel: 'Reels', engagement: 8.1 },
  { channel: 'X / Twitter', engagement: 4.3 },
  { channel: 'LinkedIn', engagement: 5.6 },
  { channel: 'Newsletter', engagement: 38.0 },
]

export const qualityMetrics = [
  { label: 'Piezas con trazabilidad completa', value: '94%' },
  { label: 'Correcciones post-publicación', value: '2' },
  { label: 'Tiempo medio de verificación', value: '31 min' },
  { label: 'Fuentes T4+ por pieza', value: '2.6' },
  { label: 'Revisiones humanas completadas', value: '100%' },
  { label: 'Incidentes editoriales abiertos', value: '1' },
]

export const incidentMetrics = [
  { label: 'Incidentes este mes', value: '3' },
  { label: 'Tiempo medio de respuesta', value: '14 min' },
  { label: 'Publicaciones retiradas', value: '0' },
  { label: 'Aclaraciones emitidas', value: '2' },
]
