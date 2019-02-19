import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { withRouter, Redirect } from 'react-router-dom'
import { Button, Grid, Form, Checkbox } from 'semantic-ui-react'
import { saveDataAction } from './accions'
import Steps from '../../components/Steps'


export class Step9 extends Component {
    state = {
        estatutoInput: null,
        balanceInput: null,
        redirectToReferrer: false,
        _loading: false,
        checked: false
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

    handleChange = (e) => this.setState({ [e.target.name]: e.target.files })

    handleSubmit = () => {
        const {
            estatutoInput,
            balanceInput,
            checked
        } = this.state

        const {
            email,
            isSociety
        } = this.props

        if (checked || (estatutoInput !== null && balanceInput !== null)) {
            this.props.handleSave({
                email: email,
                fileEstatuto: estatutoInput,
                fileBalanceInput: balanceInput,
                checked,
                isSociety
            })

            this.setState({
                _loading: true
            })
        } else {
            alert('Debe cargar archivos o seleccionar mardar despues a documentos@credility.com ')
        }
        
    }

    toggle = () => this.setState({ checked: !this.state.checked })

    render() {
        const {
            isSociety
        } = this.props

        const {
            _loading,
            redirectToReferrer
        } = this.state

        let title = 'Carga de documentos'
        let textInformative = '¡Ya casi estamos! Solo necesitamos que cargues el último balance y estatuto de tu empresa.'
        let text2 = 'Prefiero mandarlo despues a documentos@credility.com'
        let file1Title = 'BALANCE'
        let file2Title = 'ESTATUTO'

        if (!isSociety) {
            textInformative = 'Ya casi estamos! Solo necesitamos que cargues dos fotos de tu DNI'
            file1Title = 'FRENTE'
            file2Title = 'DORSO'
        }        

        if (redirectToReferrer) {
            if (isSociety) {
                return <Redirect to={{pathname: '/step10'}} />
            } else {
                return <Redirect to={{pathname: '/greeting'}} />
            }
        }

        return (
            <Grid centered>
                <Grid.Row stretched>
                    <Grid.Column>
                        <Steps step={4} rSocial={isSociety}/>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={10}>
                        <Form onSubmit={this.handleSubmit} loading={_loading}>
                            <h2 style={{color: '#092768'}}>
                                {title}
                            </h2>
                            <p>
                                { textInformative  }
                            </p>
                            
                            <br />

                            <div>
                                <label htmlFor="fileBalance" className="ui icon button">
                                    <i className="file icon"></i>
                                    {file1Title}&nbsp;
                                </label>
                                <input type="file" id='fileBalance' name='balanceInput' onChange={this.handleChange} />
                            </div>

                            <br />

                            <div>
                                <label htmlFor="fileEstatuto" className="ui icon button">
                                    <i className="file icon"></i>
                                    {file2Title}
                                </label>
                                <input type="file" id='fileEstatuto' name='estatutoInput' onChange={this.handleChange} />
                            </div>

                            <br />
                            
                            <div>
                                <Checkbox 
                                    label={ text2 }
                                    onChange={this.toggle}  
                                    checked={this.state.checked} 
                                />
                            </div>

                            <br />

                            <Button type='submit' style={{color: '#fff', background: '#EE3A43'}}>Continuar</Button>

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
    message: state.step9Reducer.messageStep9
})

const mapDispatchToProps = (dispatch) => ({
    handleSave: (payload) => dispatch(saveDataAction(payload))
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Step9))

