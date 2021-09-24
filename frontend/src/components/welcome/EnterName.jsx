import { Component, Fragment } from 'react'

import styles from './Styles'
import Button from '../Button'

import Person from '../../assets/img/person.png'
import Swal from 'sweetalert2'


class EnterName extends Component {
    constructor (props) {
        super(props)
        this.state = { name: "", isValidUsername: false }    
        this.setName = this.setName.bind(this)
        this.setIsValidUsername = this.setIsValidUsername.bind(this)
        this.checkUsername = this.checkUsername.bind(this)
    }
    
    setName (event) {
        this.setState({ name: event.target.value })
    }

    setIsValidUsername (status) {
        this.setState({ isValidUsername: status })
    }

    checkUsername(callback) {
        let url = `${ process.env.REACT_APP_BASE_API_URL }/auth/register/pipeline/?type=username&username=${ this.state.name }`;
        fetch(url, {
            method: "GET",
        })
        .then(resp => resp.json())
        .then(json => {
            if (json.hasOwnProperty('detail')) {
                this.setIsValidUsername(true)
            }
        })
        .then(() => callback())
        .catch(err => console.error(err))
    }

    render () {
        const onClickNext = () => {
            this.checkUsername(() => {
                if (!this.state.isValidUsername) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: "User with same name already exist"
                    })
                    this.setState({ name: "", isValidUsername: false })
                } else {
                    this.props.next()
                    this.props.setMeta('name', this.state.name)
                }
            })
        }
            

        return (
            <Fragment>
                <div style={styles._wrap}>
                    <div className="welcome_1 screen__center text__center" style={styles.component}>
                        <div className="welcome_1__item text-gray-800" style={styles.item}>
                            <img src={Person} alt="wave" style={styles.img} />
                            <p className="op_text">Enter your name</p>
                        </div>
                        <div><input value={this.state.name} style={styles.input} onChange={this.setName} /></div>
                        <br />
                        <p className="op_text" style={styles.min_text}>Name will be displayed in clubhouse app.</p>
                        <div className="buttons">
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Back" click={this.props.back} />
                            <Button className="btn btn-lg op_text" style={styles.btn} text="Next" click={onClickNext} />
                        </div>
                    </div>   
                </div>
            </Fragment>
        )
    }
}

export default EnterName