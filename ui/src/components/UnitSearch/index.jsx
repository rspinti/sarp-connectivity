import React, { memo, useState } from 'react'
import PropTypes from 'prop-types'

import { Text } from 'components/Text'
import { Box } from 'components/Grid'
import styled, { themeGet } from 'style'
import { useBoundsData } from 'components/Data'
import ListItem from './ListItem'
import { LAYER_NAMES, SYSTEMS, SYSTEM_UNITS } from '../../../config/constants'

const Wrapper = styled(Box)``

const Header = styled(Text)`
  font-size: 1.25rem;
`

const Input = styled.input.attrs({
  type: 'text',
})`
  width: 100%;
  border: 1px solid ${themeGet('colors.grey.500')};
  border-radius: 0.25rem;
  outline: none;
  padding: 0.25rem 0.5rem;

  &:focus {
    border-color: ${themeGet('colors.primary.500')};
  }
`

const List = styled.ul`
  list-style: none;
  margin: 0;
`

const NoResults = styled(Box).attrs({ my: '1rem' })`
  text-align: center;
  font-style: italic;
  color: ${themeGet('colors.grey.600')};
`

const UnitSearch = ({ system, layer, onSelect }) => {
  const data = useBoundsData()
  const [query, setQuery] = useState('')

  const showID = layer
    ? !(layer === 'State' || layer === 'County')
    : system !== 'ADM'

  const handleChange = ({ target: { value } }) => {
    setQuery(value)
  }

  const handleSelect = item => () => {
    onSelect(item)
    setQuery('')
  }

  let results = []
  if (query && query !== '') {
    let units = []
    if (layer !== null) {
      units = data[layer]
    } else {
      // search all layers within system
      units = SYSTEM_UNITS[system].reduce(
        (collector, systemLayer) => collector.concat(data[systemLayer]),
        []
      )
    }
    // Filter out the top 10
    try {
      // strip all special regex characters first, we don't need them here
      const expr = new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, ''), 'gi')
      const filtered = units.filter(
        ({ name, id }) =>
          name.search(expr) !== -1 || (showID && id.search(expr) !== -1)
      )
      results = filtered.slice(0, 10)
    } catch (ex) {
      console.error(ex)
    }
  }

  const searchLabel = layer ? LAYER_NAMES[layer] : SYSTEMS[system].toLowerCase()
  const suffix = ` name${
    (system && system !== 'ADM') ||
    (layer && !(layer === 'State' || layer === 'County'))
      ? ' or ID'
      : ''
  }`

  return (
    <Wrapper>
      <Header>Search for {searchLabel}:</Header>
      <Input
        placeholder={`${searchLabel}${suffix}`}
        value={query}
        onChange={handleChange}
      />
      {query !== '' && (
        <>
          {results.length > 0 ? (
            <List>
              {results.map(item => (
                <ListItem
                  key={item.id}
                  {...item}
                  showID={showID}
                  onClick={handleSelect(item)}
                />
              ))}
            </List>
          ) : (
            <NoResults>No results match your search</NoResults>
          )}
        </>
      )}
    </Wrapper>
  )
}

UnitSearch.propTypes = {
  system: PropTypes.string,
  layer: PropTypes.string,
  onSelect: PropTypes.func.isRequired,
}

UnitSearch.defaultProps = {
  layer: null,
  system: null,
}

export default memo(UnitSearch)
