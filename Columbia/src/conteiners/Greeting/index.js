import React, { Component } from 'react'
import { Grid } from 'semantic-ui-react'
import GreetingTemplate from '../../components/GreetingTemplate'

export default class Thank extends Component {
  render() {
    return (
        <Grid centered>
            <Grid.Column width={10}>
                <GreetingTemplate />
            </Grid.Column>
        </Grid>
    )
  }
}
