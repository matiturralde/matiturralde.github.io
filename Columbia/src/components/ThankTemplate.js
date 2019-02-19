import React, { Component } from 'react'

export default class ThankTemplate extends Component {
  render() {
    return (
      <div>
        <h1 style={{color: '#EE3A43'}}>¡Gracias por registrarte!</h1>
        <br />
        <h3>A la brevedad un representante se estara comunicando con usted.</h3>
        <br />
        <h3>¿Tenés alguna duda? Podés escribirnos a <a>info@credility.com</a>. </h3>
        <br />
        <br />
        <div>
        <h4>Saludos Cordiales&nbsp; <br />El equipo de Credility.</h4>
        </div>
      </div>
    )
  }
}
