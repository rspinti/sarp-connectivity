import React from 'react'
import { FaChartBar, FaSearchLocation } from 'react-icons/fa'
import { Image } from 'rebass'

import { Link } from 'components/Link'

import { Text } from 'components/Text'
import { Box, Flex } from 'components/Grid'
import styled, { themeGet } from 'style'
import LogoSVG from 'images/logo.svg'
import { siteMetadata } from '../../../gatsby-config'

const Wrapper = styled(Flex).attrs({
  as: 'header',
  alignItems: 'center',
  justifyContent: 'space-between',
  py: '0.25rem',
  px: '0.5rem',
})`
  background-color: ${themeGet('colors.primary.900')};
  flex: 0 0 auto;
  border-bottom: 4px solid ${themeGet('colors.primary.800')};
`

const SiteLogo = styled(Image).attrs({ src: LogoSVG })`
  fill: #fff;
  margin-right: 0.25rem;
  width: 1.5rem;
  height: 1.5rem;
`

const Title = styled(Text).attrs({
  as: 'h1',
  fontSize: '1.5rem',
})`
  margin: 0;
  flex: 0 0 auto;
  line-height: 1;

  & * {
    text-decoration: none;
    color: #fff !important;
  }
`

const NavBar = styled(Flex).attrs({
  alignItems: 'center',
})`
  font-size: 1rem;

  .nav-active {
    background-color: ${themeGet('colors.primary.500')};
  }
`

const NavLink = styled(Link)`
  text-decoration: none;
  padding: 0.25rem 0.5rem;
  display: block;
  color: #fff !important;
  border-radius: 6px;

  &:hover {
    background-color: ${themeGet('colors.primary.800')};
  }
`

const NavItem = styled(Flex).attrs({ alignItems: 'center' })``

const SummarizeLogo = styled(FaChartBar)`
  width: 1em;
  height: 1em;
  margin-right: 0.25em;
`

const PrioritizeLogo = styled(FaSearchLocation)`
  width: 1em;
  height: 1em;
  margin-right: 0.25em;
`

const Header = () => {
  const { title, shortTitle } = siteMetadata
  return (
    <Wrapper as="header">
      <Title>
        <Link to="/">
          <Flex alignItems="center" flexWrap="wrap">
            <Box mr="0.5rem">
              <SiteLogo />
            </Box>
            <Text display={['none', 'none', 'unset']}>{title}</Text>
            <Text display={['unset', 'unset', 'none']}>{shortTitle}</Text>
          </Flex>
        </Link>
      </Title>
      <NavBar>
        <NavLink to="/summary" activeClassName="nav-active">
          <NavItem>
            <SummarizeLogo />
            <div>Summarize</div>
          </NavItem>
        </NavLink>
        <NavLink to="/prioritize" activeClassName="nav-active">
          <NavItem>
            <PrioritizeLogo />
            <div>Prioritize</div>
          </NavItem>
        </NavLink>
      </NavBar>
    </Wrapper>
  )
}

export default Header