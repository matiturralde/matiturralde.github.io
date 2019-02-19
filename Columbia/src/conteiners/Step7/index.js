import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Grid } from 'semantic-ui-react'
import { saveDataAction } from './accions'
import Steps from '../../components/Steps'
import Instructive from '../Instructive'

export class Step7 extends Component {
    state = {
        _loading: false,
        colorButtonAfip: '#838787',
        colorButtonExterno: '#838787',
        colorButtonOtra: '#838787',
        tipoVideo: 0,
        showInst: false,
        redirectToReferrer: false
    }

    static propTypes = {
        handleSave: PropTypes.func,
        email: PropTypes.string,
        isSociety: PropTypes.bool,
        cuit: PropTypes.string,
        message: PropTypes.string
    }

    static defaultProps = {
        handleSave: () => {},
        email: '',
        isSociety: false,
        cuit: '',
        message: ''
    }

    componentWillReceiveProps(nextProps) {
        const {
            message
        } = nextProps;

        if (message === 'done') {
            this.setState({
                redirectToReferrer: true
            })
        }

    }

    handleMisComprobantes = () => {
        this.setState({
            colorButtonAfip: '#EE3A43',
            colorButtonOtra: '#838787',
            colorButtonExterno: '#838787',
            showInst: true,
            tipoVideo: 1
        })
    }

    handleOtra = () => {
        this.setState({
            colorButtonAfip: '#838787',
            colorButtonExterno: '#838787',
            colorButtonOtra: '#EE3A43',
            showInst: true,
            tipoVideo: 0
        })
    }

    handleSubmit = () => {
        const {
            tipoVideo
        } = this.state

        const {
            email
        } = this.props

        if (tipoVideo === 1) {
            this.props.handleSave({
                email: email,
                factura: 'Si',
                afip: true,
                comprobantes: true
            })
        } else if (tipoVideo === 0) {
            this.props.handleSave({
                email: email,
                factura: 'Otra',
                afip: false,
                comprobantes: false
            })
        }

        this.setState({
            _loading: true
        })
    }

    render() {
        const {
            isSociety,
            cuit
        } = this.props

        const {
            _loading,
            colorButtonAfip,
            colorButtonOtra,
            showInst,
            tipoVideo,
            redirectToReferrer
        } = this.state

        const title = 'Facturación de tu negocio'
        const textInformative = 'Elegí por favor la fuente donde registrás la mayoría de tus ventas.'

        let showInstructive = ''
        if (showInst) {
            showInstructive = (
                <Instructive 
                    cuit={cuit} 
                    tipoVideo={tipoVideo} 
                    handleSubmit={this.handleSubmit}
                    _loading={_loading}
                />
            )
        }

        if (redirectToReferrer) {
            return <Redirect to={{pathname: '/step8'}} />
        }

        return (
            <Grid centered>
                <Grid.Row stretched>
                    <Grid.Column>
                        <Steps step={2} rSocial={isSociety}/>
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
                        
                        <br />

                        <Button fluid style={{color: '#fff', background: colorButtonAfip}} onClick={this.handleMisComprobantes}>Facturación Electronica</Button>
                        
                        <br />

                        <Button fluid style={{color: '#fff', background: colorButtonOtra}} onClick={this.handleOtra}>OTRA</Button>

                        <br />
                        
                        { showInstructive }

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

const mapStateToProps = (state) => ({
    email: state.step1Reducer.email,
    isSociety: state.step4Reducer.isSociety,
    cuit: state.step4Reducer.cuit,
    message: state.step7Reducer.messageStep7,
})

const mapDispatchToProps = (dispatch) => ({
    handleSave: (payload) => dispatch(saveDataAction(payload)),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step7))