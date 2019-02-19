import React, { Component } from 'react'

export default class GreetingTemplate extends Component {
  render() {
    return (
      <div>
        <h1 style={{color: '#EE3A43'}}>¡Muchas gracias por completar todos los datos!</h1>
        <br />
        <h3>¿No fue tanto trabajo, no? Con la información que nos diste ya estamos calificando tu negocio. En las próximas 24hs horas te vamos hacer una oferta de línea de crédito. </h3>
        <br />
        <h3>¿Tenés alguna duda? Podés escribirnos a <a>info@credility.com</a>. </h3>
        <h3>Si querés conocer un poco más de Credility podés leer nuestro <a href="https://blog.credility.com/">Blog</a></h3>
        <br />
        <br />
        <div>
        <h4>Saludos Cordiales&nbsp; <br />El equipo de Credility.</h4>
        </div>
      </div>
    )
  }
}
