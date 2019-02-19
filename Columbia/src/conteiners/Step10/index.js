import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Grid, Form, Icon } from 'semantic-ui-react'
import { saveDataAction } from './accions'
import Steps from '../../components/Steps'

export class Step10 extends Component {
    state = {
        socios: [{
            cuit: '',
            nombre: '',
            porcentaje: ''
        }],
        totalPorcentaje: 0,
        cuilLength: true,
        redirectToReferrer: false,
        _loading: false
    }

    static propTypes = {
        handleSave: PropTypes.func,
        email: PropTypes.string,
        isSociety: PropTypes.bool,
        message: PropTypes.string
    }

    static defaultProps = {
        email: '',
        isSociety: false,
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

    handlePlus = () => {
        let {
            socios
        } = this.state

        socios.push({
            cuit: '',
            nombre: '',
            porcentaje: ''
        });

        this.setState({
            socios
        })
    }

    handleChange = (e,index) => {
        let {
            socios
        } = this.state

        const saveSocios = socios.map((socio, i) => {
            if (i === index['data-key']) {
                return {
                    ...socio,
                    [e.target.name]: e.target.value
                }
            }
            return socio
        })

        this.setState({
            socios: saveSocios
        }, () => {
            this.validateInput()
        })
    }

    handleDelete = (e, index) => {
        let {
            socios
        } = this.state

        const deleteSocios = socios.filter((socio, i) => {
                    if (i !== index['data-key']) {
                        return socio
                    }
                })

        this.setState({
            socios: deleteSocios
        })
    }

    validateInput = () => {
        let {
            socios
        } = this.state

        let total = 0
        let cLength = true

        socios.forEach(item => {
            total = parseInt(item.porcentaje) + total
            if (item.cuit.length < 11) {
                cLength = false
            } 
        })

        this.setState({
            totalPorcentaje: total,
            cuilLength: cLength
        })
    }

    handleSubmit = () => {
        const {
            socios,
            cuilLength,
            totalPorcentaje
        } = this.state

        const {
            email
        } = this.props

        if (totalPorcentaje === 100 && cuilLength ) {
            this.props.handleSave({
                email: email,
                socios
            })

            this.setState({
                _loading: true
            })
        } else {
            alert('La suma de porcentaje debe ser igual 100 y la longitud de cuit debe ser igual a 11')
        }
        
    }

    render() {
        const {
            isSociety,
        } = this.props

        const {
            _loading,
            socios,
            redirectToReferrer
        } = this.state

        const title = '¿Quiénes son los socios de la empresa?'
        const textInformative = 'Solo para estar seguros de que el Estatuto está actualizado. ¿Nos podés decir por favor los CUITs y participaciones accionarias de los socios actuales?'
        
        let list = socios.map((item, index) => {
            return (
                <Form.Group key={index} widths='equal'>

                    <Form.Input fluid label='CUIT' name='cuit' placeholder='CUIT' onChange={(e,index) => this.handleChange(e,index)} data-key={index}/>

                    <Form.Input fluid label='Nombre' name='nombre' placeholder='Nombre' onChange={(e,index) => this.handleChange(e,index)} data-key={index} />

                    <Form.Input fluid label='Porcentaje %' name='porcentaje' placeholder='%' onChange={(e,index) => this.handleChange(e,index)} data-key={index} />

                    <div>  
                        <Button icon size='medium' style={{marginTop: '55%'}} onClick={(e,index) => this.handleDelete(e,index)} data-key={index}>
                            <Icon name='trash alternate' />
                        </Button>
                    </div>

                </Form.Group>
            )
        })

        if (redirectToReferrer) {
            return <Redirect to={{pathname: '/greeting'}} />
        }

        return (
            <Grid centered>
                <Grid.Row stretched>
                    <Grid.Column>
                        <Steps step={5} rSocial={isSociety}/>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={10}>
                        <Form loading={_loading}>
                            <h3>
                                {title}
                            </h3>
                            <p>
                                { textInformative  }
                            </p>
                            
                            { list }

                            <br />

                            <Button type='button' icon='plus' content='Agregar Socio' onClick={this.handlePlus} />
                            
                            <div style={{marginTop: '10%'}} />

                            <Button onClick={this.handleSubmit} style={{color: '#fff', background: '#EE3A43'}}>Terminar</Button>

                        </Form>

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

const mapStateToProps = (state) => ({
    email: state.step1Reducer.email,
    isSociety: state.step4Reducer.isSociety,
    message: state.step10Reducer.messageStep10
})

const mapDispatchToProps = (dispatch) => ({
    handleSave: (payload) => dispatch(saveDataAction(payload))
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step10))
