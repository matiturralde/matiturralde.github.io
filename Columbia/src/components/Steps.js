
import React, { Component } from 'react'
import { Step } from 'semantic-ui-react'

const titles = [
  'Datos Básicos',
  'Contacto',
  'Facturación',
  'Identidad',
  'Documentos',
  'Socios'
]

const titlesMono = [
  'Datos Básicos',  
  'Contacto',
  'Facturación',
  'Identidad',
  'Documentos'
]

export default class Steps extends Component {
  render() {

    const arrayTitle = this.props.rSocial ? titles : titlesMono

    const steps = arrayTitle.map((title, index) => {
                    if (index < this.props.step) {
                      return (
                        <Step key={index} completed>
                          <Step.Content>
                            <Step.Title>{title}</Step.Title>
                          </Step.Content>
                        </Step>        
                      )
                    } else {
                      if (index === this.props.step) {
                        return (
                          <Step key={index} active>
                            <Step.Content>
                              <Step.Title>{title}</Step.Title>
                            </Step.Content>
                          </Step>        
                        )
                      }
                    }
                    return (
                      <Step key={index} disabled>
                        <Step.Content>
                          <Step.Title>{title}</Step.Title>
                        </Step.Content>
                      </Step>        
                    )
                  })

    return (
      <Step.Group ordered size='tiny'>
        { steps }
      </Step.Group>
    )
  }
}