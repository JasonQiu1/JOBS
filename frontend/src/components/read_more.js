import React, { useState } from 'react';
import PropTypes from 'prop-types';
import TruncateMarkup from 'react-truncate-markup';
import { Link } from 'react-router-dom';

interface MyProps {}
export default function ReadMore(props:React.PropsWithChildren<MyProps>) {
    const [expanded, setExpanded] = useState(false);
    const [truncated, setTruncated] = useState("");
 
    const toggleLines = (e) => {
        // DON'T USE PREVENT DEFAULT, NEED TO REDIRECT TO WORK
        setExpanded(!expanded);
    }

    return (
        <a href={"#" + props.id} key={props.id + 'link'} style={{"textDecoration":"none", color:"black"}} onClick={toggleLines}>
                {expanded ? props.children : (
                    <TruncateMarkup
                        lines={props.lines}
                        ellipsis="..."
                    >
                        {props.children}
                    </TruncateMarkup>)}
                <p><em>Click anywhere to read more or less!</em></p>
        </a>
    );
};
