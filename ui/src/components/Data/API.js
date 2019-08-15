import { csvParse, autoType } from 'd3-dsv'

import { captureException } from 'util/log'
import { siteMetadata } from '../../../gatsby-config'

const { apiHost } = siteMetadata

/**
 * Converts units and filters into query parameters for API requests
 * @param {Array} units - array of objects with id property
 * @param {Map} filters - map of filter values, where filter name is key
 */
const apiQueryParams = (units = [], filters = {}) => {
  const ids = units.map(({ id }) => id)
  const filterValues = Object.entries(filters).filter(([, v]) => v.size > 0)

  if (!(ids.length || filterValues.length)) return ''

  let query = `id=${ids.join(',')}`

  if (filterValues.length > 0) {
    query += `&${filterValues
      .map(([k, v]) => `${k}=${Array.from(v).join(',')}`)
      .join('&')}`
  }

  return query
}

const fetchCSV = async (url, options, rowParser) => {
  try {
    const request = await fetch(url, options)
    if (request.status !== 200) {
      throw new Error(`Failed request to ${url}: ${request.statusText}`)
    }

    const rawContent = await request.text()

    return {
      error: null,
      csv: csvParse(rawContent, rowParser),
    }
  } catch (err) {
    captureException(err)

    return {
      error: err,
      csv: null,
    }
  }
}

/**
 * Fetch and parse CSV data from API for dams or small barriers
 */
export const fetchBarrierInfo = async (barrierType, layer, summaryUnits) => {
  const url = `${apiHost}/api/v1/${barrierType}/query/${layer}?${apiQueryParams(
    summaryUnits
  )}`

  return fetchCSV(url, undefined, autoType)
}

/**
 * Fetch and parse CSV data from API for dams or small barriers
 */
export const fetchBarrierRanks = async (
  barrierType,
  layer,
  summaryUnits,
  filters
) => {
  const url = `${apiHost}/api/v1/${barrierType}/rank/${layer}?${apiQueryParams(
    summaryUnits,
    filters
  )}`

  return fetchCSV(url, undefined, autoType)
}

export const getDownloadURL = (barrierType, layer, summaryUnits, filters) =>
  `${apiHost}/api/v1/${barrierType}/csv/${layer}?${apiQueryParams(
    summaryUnits,
    filters
  )}`