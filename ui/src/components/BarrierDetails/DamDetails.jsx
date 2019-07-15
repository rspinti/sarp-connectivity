import React from 'react'
import PropTypes from 'prop-types'

import { formatNumber } from 'util/format'
import { isEmptyString } from 'util/string'
import { Section, SectionHeader, List } from './styles'

import {
  DAM_CONDITION,
  CONSTRUCTION,
  PURPOSE,
  RECON,
  SINUOSITY,
} from '../../../config/constants'

const DamDetails = ({
  sarpid,
  lat,
  lon,
  hasnetwork,
  height,
  nidid,
  source,
  year,
  construction,
  purpose,
  condition,
  river,
  basin,
  rarespp,
  recon,
  // metrics
  gainmiles,
  upstreammiles,
  downstreammiles,
  sinuosity,
  landcover,
  sizeclasses,
}) => (
  <div id="BarrierDetails">
    <Section>
      <SectionHeader>Location</SectionHeader>
      <List>
        <li>
          Coordinates: {formatNumber(lat, 3)}
          &deg; N, {formatNumber(lon, 3)}
          &deg; E
        </li>
        <li>
          {river && river !== 'null' && river !== 'Unknown'
            ? `${river}, `
            : null}
          {basin} Basin
        </li>
      </List>
    </Section>

    <Section>
      <SectionHeader>Construction information</SectionHeader>
      <List>
        <li>Barrier type: dam</li>
        {year > 0 ? <li>Constructed completed: {year}</li> : null}
        {height > 0 ? <li>Height: {height} feet</li> : null}
        {construction && CONSTRUCTION[construction] ? (
          <li>
            Construction material: {CONSTRUCTION[construction].toLowerCase()}
          </li>
        ) : null}
        {purpose && PURPOSE[purpose] ? (
          <li>Purpose: {PURPOSE[purpose].toLowerCase()}</li>
        ) : null}
        {condition && DAM_CONDITION[condition] ? (
          <li>
            Structural condition: {DAM_CONDITION[condition].toLowerCase()}
          </li>
        ) : null}
      </List>
    </Section>

    <Section>
      <SectionHeader>Functional network information</SectionHeader>

      <List>
        {hasnetwork ? (
          <>
            <li>
              <b>{formatNumber(gainmiles)}</b> miles could be gained by removing
              this barrier
              <List>
                <li>
                  {formatNumber(upstreammiles)} miles in the upstream network
                </li>
                <li>
                  {formatNumber(downstreammiles)} miles in the downstream
                  network
                </li>
              </List>
            </li>
            <li>
              <b>{sizeclasses}</b> river size{' '}
              {sizeclasses === 1 ? 'class' : 'classes'} could be gained by
              removing this barrier
            </li>
            <li>
              <b>{formatNumber(landcover, 0)}%</b> of the upstream floodplain is
              composed of natural landcover
            </li>
            <li>
              The upstream network has <b>{SINUOSITY[sinuosity]}</b> sinuosity
            </li>
          </>
        ) : (
          <li className="has-text-grey">
            This barrier is off-network and has no functional network
            information.
          </li>
        )}
      </List>
    </Section>

    <Section>
      <SectionHeader>Species information</SectionHeader>
      <List>
        {rarespp > 0 ? (
          <>
            <li>
              <b>{rarespp}</b> threatened and endangered aquatic species have
              been found in the subwatershed containing this barrier.
            </li>
            <li className="has-text-grey is-size-7">
              Note: species information is very incomplete. These species may or
              may not be directly impacted by this barrier.
            </li>
          </>
        ) : (
          <li className="has-text-grey">
            No threatened and endangered aquatic species have been identified by
            available data sources for this subwatershed.
          </li>
        )}
      </List>
    </Section>

    <Section>
      <SectionHeader>Feasibility & Conservation Benefit</SectionHeader>
      <List>
        {recon !== null ? (
          <li>{RECON[recon]}</li>
        ) : (
          <li className="has-text-grey">
            No feasibility information is available for this barrier.
          </li>
        )}
      </List>
    </Section>

    <Section>
      <SectionHeader>Other information</SectionHeader>
      <List>
        <li>SARP ID: {sarpid}</li>
        {!isEmptyString(nidid) ? (
          <li>
            National inventory of dams ID:{' '}
            <a
              href="http://nid.usace.army.mil/cm_apex/f?p=838:12"
              target="_blank"
              rel="noopener noreferrer"
            >
              {nidid}
            </a>
          </li>
        ) : null}

        {!isEmptyString(source) ? <li>Source: {source}</li> : null}
      </List>
    </Section>
  </div>
)

DamDetails.propTypes = {
  sarpid: PropTypes.number.isRequired,
  lat: PropTypes.number.isRequired,
  lon: PropTypes.number.isRequired,
  hasnetwork: PropTypes.bool.isRequired,
  river: PropTypes.string,
  basin: PropTypes.string.isRequired,
  height: PropTypes.number,
  year: PropTypes.number,
  nidid: PropTypes.string,
  source: PropTypes.string,
  construction: PropTypes.number,
  purpose: PropTypes.number,
  condition: PropTypes.number,
  rarespp: PropTypes.number,
  recon: PropTypes.number,
  gainmiles: PropTypes.number,
  upstreammiles: PropTypes.number,
  downstreammiles: PropTypes.number,
  sinuosity: PropTypes.number,
  landcover: PropTypes.number,
  sizeclasses: PropTypes.number,
}

DamDetails.defaultProps = {
  river: null,
  nidid: null,
  source: null,
  height: 0,
  year: 0,
  construction: 0,
  purpose: 0,
  condition: 0,
  rarespp: 0,
  recon: 0,
  gainmiles: null,
  upstreammiles: null,
  downstreammiles: null,
  sinuosity: null,
  landcover: null,
  sizeclasses: null,
}

export default DamDetails
