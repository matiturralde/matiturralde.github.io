import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter } from 'react-router-dom'
import { Grid } from 'semantic-ui-react'
import Steps from '../../components/Steps'

import { friendlyScore } from '../../utils/friendlyScore'

export class Step8 extends Component {
    state = {}

    static propTypes = {
        email: PropTypes.string,
        isSociety: PropTypes.bool
    }

    static defaultProps = {
        email: '',
        isSociety: false
    }

    componentDidMount() {
        friendlyScore()
    }

    render() {
        const {
            isSociety
        } = this.props

        const title = 'Validación de identidad'
        const textInformative = 'Haciendo click en el siguiente botón, te vamos a pedir que te loguees con alguna/s de tus redes sociales personales. De esta forma podemos confirmar tu identidad sin necesidad de conocerte personalmente.'
        const text2 = '¡Cuantas más redes selecciones, mejor va ser tu calificación! Recordá que en Credility no vemos contraseñas ni compartimos datos sensibles.'
        
        return (
            <Grid centered>
                <Grid.Row stretched>
                    <Grid.Column>
                        <Steps step={3} rSocial={isSociety}/>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={10}>
                        <h2 style={{color: '#092768'}}>
                            {title}
                        </h2>
                        <p>
                            { textInformative  }
                        </p>
                        <p>
                            { text2  }
                        </p>
                        
                        <br />
                        
                        <br />

                        <div id="fs-widget-btn" data-fs-btn-size="medium" data-fs-lang="es" data-fs-button-text="Validar Identidad" data-fs-app-id="1287"></div>



                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

const mapStateToProps = (state) => ({
    email: state.step1Reducer.email,
    isSociety: state.step4Reducer.isSociety
})

const mapDispatchToProps = (dispatch) => ({})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step8))
