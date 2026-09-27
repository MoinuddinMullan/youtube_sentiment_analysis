import { useEffect, useRef, useState } from 'react'

export function useCountUp(target, duration = 1400, delay = 0) {
  const [value, setValue] = useState(0)
  const startTime = useRef(null)
  const rafId = useRef(null)

  useEffect(() => {
    if (target === 0 || target === null || target === undefined) {
      setValue(0)
      return
    }

    const startAnimation = () => {
      startTime.current = null

      const step = timestamp => {
        if (startTime.current === null) startTime.current = timestamp
        const progress = Math.min((timestamp - startTime.current) / duration, 1)
        const eased = 1 - Math.pow(1 - progress, 3)
        setValue(Math.floor(eased * target))

        if (progress < 1) {
          rafId.current = requestAnimationFrame(step)
        } else {
          setValue(target)
        }
      }

      rafId.current = requestAnimationFrame(step)
    }

    const timer = setTimeout(startAnimation, delay)
    return () => {
      clearTimeout(timer)
      if (rafId.current !== null) cancelAnimationFrame(rafId.current)
    }
  }, [target, duration, delay])

  return value.toLocaleString()
}