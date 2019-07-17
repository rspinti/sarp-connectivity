import React, { useState, useCallback, useRef } from 'react'

import { HelpText } from 'components/Text'
import { Flex } from 'components/Grid'
import Sidebar, { LoadingSpinner, ErrorMessage } from 'components/Sidebar'
import BarrierDetails from 'components/BarrierDetails'
import styled from 'style'

import Map from './Map'
import UnitChooser from './UnitChooser'
import LayerChooser from './LayerChooser'
import BarrierFilters from './BarrierFilters'

const Wrapper = styled(Flex)`
  height: 100%;
`

const MapContainer = styled.div`
  position: relative;
  flex: 1 0 auto;
  height: 100%;
`

const Prioritize = () => {
  const [selectedBarrier, setSelectedBarrier] = useState(null)
  const [searchFeature, setSearchFeature] = useState(null)
  const [summaryUnits, setSummaryUnits] = useState([]) // useState([{"id":"Arkansas","dams":6269,"off_network_dams":422,"miles":10.72599983215332,"barriers":3018,"off_network_barriers":1526,"layerId":"State"}]) // FIXME
  const [filters, setFilters] = useState(null)

  // TODO: wrap into useReducer?
  const [step, setStep] = useState('select')
  const stepRef = useRef(step) // need to keep a ref to use in callback below
  const [layer, setLayer] = useState(null) // useState('State') // FIXME

  // TODO: wrap into custom hook
  const [isLoading, setIsLoading] = useState(true)
  const [isError, setIsError] = useState(false)

  // keep the reference in sync
  stepRef.current = step

  const handleMapLoad = useCallback(() => {
    setIsLoading(false)
  })

  const handleSearch = useCallback(
    nextSearchFeature => {
      setSearchFeature(nextSearchFeature)
    },
    [layer]
  )

  const handleSetLayer = nextLayer => {
    setSearchFeature(null)
    setSummaryUnits([])
    setFilters(null)
    setLayer(nextLayer)
  }

  // Toggle selected unit in or out of selection
  const handleSelectUnit = unit => {
    const { id } = unit

    setSummaryUnits(prevSummaryUnits => {
      // NOTE: we are always creating a new object,
      // because we cannot mutate the underlying object
      // without causing the setSummaryUnits call to be a no-op
      const index = prevSummaryUnits.findIndex(
        ({ id: unitId }) => unitId === id
      )

      if (index === -1) {
        // add it
        return prevSummaryUnits.concat([unit])
      }

      // remove it
      return prevSummaryUnits
        .slice(0, index)
        .concat(prevSummaryUnits.slice(index + 1))
    })

    setFilters(null)
    setSearchFeature(null)
  }

  const handleFilterChange = newFilters => {
    setFilters(newFilters)
  }

  

  // WARNING: this is passed into map at construction type, any 
  // local state referenced here is not updated when the callback
  // is later called.  To get around that, use reference to step instead.
  const handleSelectBarrier = feature => {
    const {current: curStep} = stepRef
    // don't show details when selecting units
    if (curStep === 'select') return

    console.log('selected feature', feature)

    setSelectedBarrier(feature)
  }

  const handleDetailsClose = () => {
    setSelectedBarrier(null)
  }
 
  let sidebarContent = null

  if (selectedBarrier === null) {
    if (isError) {
      // TODO
      sidebarContent = (
        <ErrorMessage>
          There was an error loading these data. Please refresh your browser
          page and try again.
          <HelpText fontSize="1rem" mt="2rem">
            If it happens again, please{' '}
            <a href="mailto:kat@southeastaquatics.net">contact us</a>.
          </HelpText>
        </ErrorMessage>
      )
    } else if (isLoading) {
      // TODO
      sidebarContent = (
        <LoadingSpinner />
        // <div className="loading-spinner flex-container flex-justify-center flex-align-center">
        //   <div className="fas fa-sync fa-spin" />
        //   <p>Loading...</p>
        // </div>
      )
    } else {
      switch (step) {
        case 'select': {
          if (layer === null) {
            sidebarContent = <LayerChooser setLayer={handleSetLayer} />
          } else {
            sidebarContent = (
              <UnitChooser
                layer={layer}
                summaryUnits={summaryUnits}
                onBack={() => handleSetLayer(null)}
                selectUnit={handleSelectUnit}
                setSearchFeature={handleSearch}
                onSubmit={() => setStep('filter')}
              />
            )
          }
          break
        }
        case 'filter': {
          sidebarContent = (
            <BarrierFilters
              layer={layer}
              summaryUnits={summaryUnits}
              onBack={() => setStep('select')}
              onFilterChange={handleFilterChange}
              onSubmit={() => setStep('results')}
            />
          )
          break
        }
        default: {
          sidebarContent = null
        }

        // case "results": {
        //     sidebarContent = <Results />
        //     break
        // }
      }
    }
  }

  return (
    <Wrapper>
      <Sidebar>
        {selectedBarrier !== null ? (
          <BarrierDetails
            barrier={selectedBarrier}
            onClose={handleDetailsClose}
          />
        ) : (
          sidebarContent
        )}
      </Sidebar>

      <MapContainer>
        <Map
          allowUnitSelect={step === 'select'}
          allowFilter={step === 'filter'}
          step={step}
          activeLayer={layer}
          searchFeature={searchFeature}
          selectedBarrier={selectedBarrier}
          summaryUnits={summaryUnits}
          filters={filters}
          onSelectUnit={handleSelectUnit}
          onSelectBarrier={handleSelectBarrier}
          onMapLoad={handleMapLoad}
        />
      </MapContainer>
    </Wrapper>
  )
}

export default Prioritize
