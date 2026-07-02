import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center gap-1 rounded-md border px-1.5 py-0.5 text-2xs font-medium leading-4 whitespace-nowrap',
  {
    variants: {
      variant: {
        neutral: 'border-line bg-white/5 text-ink-secondary',
        cyan: 'border-accent-cyan/30 bg-accent-cyan/10 text-accent-cyan',
        green: 'border-accent-green/30 bg-accent-green/10 text-accent-green',
        yellow: 'border-accent-yellow/30 bg-accent-yellow/10 text-accent-yellow',
        orange: 'border-accent-orange/30 bg-accent-orange/10 text-accent-orange',
        red: 'border-accent-red/30 bg-accent-red/10 text-accent-red',
        purple: 'border-accent-purple/30 bg-accent-purple/10 text-accent-purple',
        blue: 'border-accent-blue/30 bg-accent-blue/10 text-accent-blue',
      },
    },
    defaultVariants: {
      variant: 'neutral',
    },
  },
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
