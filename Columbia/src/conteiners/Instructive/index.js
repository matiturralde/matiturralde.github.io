import React, { Component } from 'react'
import { Button } from 'semantic-ui-react'

import YouTube from '../../components/YouTube'

export default class index extends Component {
  
    render() {
        const {
            tipoVideo
        } = this.props        

        let textInformative = 'Con el siguiente instructivo nos podés dar acceso para que veamos las ventas de tu negocio que declaraste en la AFIP. Esto nos permite hacerte una oferta de crédito actualizada.'
        let text2 = 'El proceso es totalmente seguro y en ningún momento vemos tu clave fiscal. Una vez que hayas hecho la delegación, clickea en "Continuar" para continuar con la solicitud.'
        
        
        let video = ''
        if (tipoVideo === 1) {
            video = (
                <YouTube video="jj6_uWeE7Sw" autoplay="0" rel="0" modest="1" />
            )
        } else if (tipoVideo === 2) {
            video = (
                <YouTube video="NyhO-8bELdg" autoplay="0" rel="0" modest="1" />
            )
        } else if (tipoVideo === 0) {
            textInformative = 'Al finalizar el proceso de aplicación, por favor envíanos a documentos@credility.com los comprobantes de ventas de los últimos 12 meses (pueden ser las Declaraciones Juradas de IVA, presentaciones de Ingresos Brutos, etc.)'
            text2 = ''
        }

        return (
            <div>
                <hr />
                <br />
                <p>
                    { textInformative  }
                </p>
                <p>
                    { text2  }
                </p>

                <br />
                
                { video }
            
                <p />

                <Button style={{color: '#fff', background: '#EE3A43'}} onClick={this.props.handleSubmit} loading={this.props._loading}>Continuar</Button>
            
                <br />

            </div>
        )
    }
}
