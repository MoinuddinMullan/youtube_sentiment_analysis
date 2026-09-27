export const formatNumber = (num) => {
  if (num === null || num === undefined) return '0'
  return new Intl.NumberFormat('en-US').format(num)
}

export const formatPercent = (decimal) => {
  if (decimal === null || decimal === undefined) return '0%'
  return (decimal * 100).toFixed(1) + '%'
}

export const formatDate = (isoString) => {
  if (!isoString) return ''
  return new Date(isoString).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: 'numeric', minute: 'numeric'
  })
}

export const truncate = (str, len = 100) => {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '...' : str
}
