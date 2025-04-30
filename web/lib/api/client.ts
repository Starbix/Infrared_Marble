import axios from 'axios'

/**
 * Use to mutate data
 */
export const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL
})

/**
 * For use with useSWR
 */
export const fetcher = url => client.get(url).then(res => res.data)
