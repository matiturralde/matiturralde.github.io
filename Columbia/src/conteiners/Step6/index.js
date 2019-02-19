import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Grid } from 'semantic-ui-react'
import { sendEmailAction } from './accions'

export class Step6 extends Component {
    state = {
        redirectToNextStep: false,
        redirectToThank: false,
        _loadingPhone: false,
        _loadingNext: false
    }
  
    static propTypes = {
        handleSendEmail: PropTypes.func,
        email: PropTypes.any,
        message: PropTypes.any
    }

    static defaultProps = {
        email: '',
        message: ''
    }

    componentWillReceiveProps(nextProps) {
        const {
            message
        } = nextProps;

        if (message === 'prefiere que lo llamen') {
            this.setState({
                redirectToThank: true
            })
        } 
        
        if (message === 'continua los step') {
            this.setState({
                redirectToNextStep: true
            })
        }

    }

    handlePhone = () => {
        const {
            email
        } = this.props

        this.props.handleSendEmail({
            email,
            seleccion: 'prefiere que lo llamen'
        })
        this.setState({
            _loadingPhone: true
        })
    }

    handleNext = () => {
        const {
            email
        } = this.props

        this.props.handleSendEmail({
            email,
            seleccion: 'continua los step'
        })
        this.setState({
            _loadingNext: true
        })
    }

    render() {
    const {
        redirectToNextStep,
        redirectToThank,
        _loadingNext,
        _loadingPhone
    } = this.state 
    
    const title = '¿Querés tener una respuesta a tu solicitud mañana?'
    const textInformative = '¡Ya estás a mitad de camino! Ahora vamos a necesitar un poco de información financiera de tu empresa para calificar tu negocio y hacerte una oferta de crédito.'
    const text2 = '¡Si la cargás ahora te vamos a dar una respuesta en 24hs! Si preferís, te podemos llamar para seguir con el proceso otro día.'

    if (redirectToNextStep) {
        return <Redirect to={{pathname: '/step7'}} />;
    }

    if (redirectToThank) {
        return <Redirect to={{pathname: '/thank'}} />;
    }

    return (
        <Grid centered>
            <Grid.Row>
                <Grid.Column width={10}>
                    <h2 style={{color: '#EE3A43'}}>
                        {title}
                    </h2>
                    
                    <p>
                        { textInformative  }
                    </p>
                    <p>
                        { text2  }
                    </p>
                    
                    <br />

                    <Button fluid style={{color: '#fff', background: '#EE3A43'}} onClick={this.handleNext} loading={_loadingNext}>QUIERO SEGUIR AHORA Y TENER UNA RESPUESTA RAPIDA</Button>

                    <br />

                    <Button fluid style={{color: '#fff', background: '#838787'}} onClick={this.handlePhone} loading={_loadingPhone}>PREFIERO QUE ME LLAMEN Y SEGUIR OTRO DIA</Button>
                    
                    <br />

                </Grid.Column>
            </Grid.Row>
        </Grid>
    )
  }
}

const mapStateToProps = (state) => ({
    email: state.step1Reducer.email,
    message: state.step6Reducer.messageStep6,
})

const mapDispatchToProps = (dispatch) => ({
    handleSendEmail: (payload) => dispatch(sendEmailAction(payload)),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step6))