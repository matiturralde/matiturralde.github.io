import React, { Component } from 'react'
import { Grid } from 'semantic-ui-react'
import ThankTemplate from '../../components/ThankTemplate'

export default class Thank extends Component {
  render() {
    return (
        <Grid centered>
            <Grid.Column width={10}>
                <ThankTemplate />
            </Grid.Column>
        </Grid>
    )
  }
}
