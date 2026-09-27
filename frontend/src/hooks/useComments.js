import { useState } from 'react'

export const useComments = (initialComments = []) => {
  const [comments, setComments] = useState(initialComments)

  // Could add pagination/filtering logic here later if needed client-side

  return { comments, setComments }
}
