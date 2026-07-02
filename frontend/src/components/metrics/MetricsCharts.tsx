import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import {
  AXIS_STROKE,
  ChartLegend,
  ChartTooltip,
  GRID_STROKE,
  SERIES,
  STATUS,
  SURFACE,
  TICK_STYLE,
} from './chart-theme'
import {
  agentRunsByDay,
  engagementByChannel,
  productionByDay,
  publicationsByChannel,
  risksByCategory,
  verificationTime,
} from '@/data/mock-metrics'

const axisProps = {
  tick: TICK_STYLE,
  tickLine: false,
  axisLine: { stroke: AXIS_STROKE },
} as const

function ChartCard({
  title,
  description,
  children,
  legend,
}: {
  title: string
  description: string
  children: React.ReactNode
  legend?: { label: string; color: string }[]
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        {legend && <ChartLegend items={legend} />}
        <div className="h-52">{children}</div>
      </CardContent>
    </Card>
  )
}

export function ProductionChart() {
  return (
    <ChartCard
      title="Producción por día"
      description="Piezas redactadas vs publicadas (datos de demostración)"
      legend={[
        { label: 'Redactadas', color: SERIES[1] },
        { label: 'Publicadas', color: SERIES[2] },
      ]}
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={productionByDay} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis dataKey="day" {...axisProps} />
          <YAxis {...axisProps} />
          <Tooltip content={<ChartTooltip />} cursor={{ stroke: AXIS_STROKE }} />
          <Line type="monotone" dataKey="drafted" name="Redactadas" stroke={SERIES[1]} strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
          <Line type="monotone" dataKey="published" name="Publicadas" stroke={SERIES[2]} strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  )
}

export function PublicationsByChannelChart() {
  return (
    <ChartCard
      title="Publicaciones por canal"
      description="Últimos 7 días (datos de demostración)"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={publicationsByChannel} margin={{ top: 4, right: 8, left: -20, bottom: 14 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis
            dataKey="channel"
            {...axisProps}
            interval={0}
            angle={-32}
            textAnchor="end"
            tick={{ ...TICK_STYLE, fontSize: 10 }}
          />
          <YAxis {...axisProps} />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
          <Bar dataKey="count" name="Publicaciones" fill={SERIES[1]} radius={[4, 4, 0, 0]} maxBarSize={28} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  )
}

export function RisksByCategoryChart() {
  return (
    <ChartCard
      title="Riesgos por categoría"
      description="Distribución por nivel de riesgo (datos de demostración)"
      legend={[
        { label: 'Critical', color: STATUS.critical },
        { label: 'High', color: STATUS.serious },
        { label: 'Medium', color: STATUS.warning },
        { label: 'Low', color: STATUS.good },
      ]}
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={risksByCategory} margin={{ top: 4, right: 8, left: -20, bottom: 14 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis
            dataKey="category"
            {...axisProps}
            interval={0}
            angle={-32}
            textAnchor="end"
            tick={{ ...TICK_STYLE, fontSize: 10 }}
          />
          <YAxis {...axisProps} />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
          <Bar dataKey="low" name="Low" stackId="r" fill={STATUS.good} stroke={SURFACE} strokeWidth={2} maxBarSize={28} />
          <Bar dataKey="medium" name="Medium" stackId="r" fill={STATUS.warning} stroke={SURFACE} strokeWidth={2} maxBarSize={28} />
          <Bar dataKey="high" name="High" stackId="r" fill={STATUS.serious} stroke={SURFACE} strokeWidth={2} maxBarSize={28} />
          <Bar dataKey="critical" name="Critical" stackId="r" fill={STATUS.critical} stroke={SURFACE} strokeWidth={2} radius={[4, 4, 0, 0]} maxBarSize={28} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  )
}

export function AgentRunsChart() {
  return (
    <ChartCard title="Agentes ejecutados" description="Ejecuciones por día (datos de demostración)">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={agentRunsByDay} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis dataKey="day" {...axisProps} />
          <YAxis {...axisProps} />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
          <Bar dataKey="runs" name="Ejecuciones" fill={SERIES[4]} radius={[4, 4, 0, 0]} maxBarSize={28} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  )
}

export function VerificationTimeChart() {
  return (
    <ChartCard
      title="Tiempo promedio de verificación"
      description="Minutos por día (datos de demostración)"
    >
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={verificationTime} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <CartesianGrid stroke={GRID_STROKE} vertical={false} />
          <XAxis dataKey="day" {...axisProps} />
          <YAxis {...axisProps} />
          <Tooltip content={<ChartTooltip />} cursor={{ stroke: AXIS_STROKE }} />
          <Line type="monotone" dataKey="minutes" name="Minutos" stroke={SERIES[1]} strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  )
}

export function EngagementChart() {
  return (
    <ChartCard
      title="Engagement por canal"
      description="Tasa de interacción % (datos de demostración)"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={engagementByChannel} layout="vertical" margin={{ top: 4, right: 16, left: 10, bottom: 0 }}>
          <CartesianGrid stroke={GRID_STROKE} horizontal={false} />
          <XAxis type="number" {...axisProps} />
          <YAxis type="category" dataKey="channel" width={80} {...axisProps} tick={{ ...TICK_STYLE, fontSize: 10 }} />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
          <Bar dataKey="engagement" name="Engagement %" fill={SERIES[5]} radius={[0, 4, 4, 0]} maxBarSize={16} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  )
}
