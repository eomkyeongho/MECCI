import React, { Children } from 'react'
import ModalDialog from './ModalDialog'

const Validate = ({ props }) => {
    const { open, close } = { props };

    return (
        <ModalDialog
            open={open}
            handleClose={close}
        ></ModalDialog>
    )
}

export default Validate;