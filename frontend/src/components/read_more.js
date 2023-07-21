import React, { useState } from 'react';
import PropTypes from 'prop-types';
import TruncateMarkup from 'react-truncate-markup';
import { Link } from 'react-router-dom';

interface MyProps {}
export default function ReadMore(props:React.PropsWithChildren<MyProps>) {
    const [expanded, setExpanded] = useState(false);
    const [truncated, setTruncated] = useState("");
 
    const toggleLines = (e) => {
        e.preventDefault();
        setExpanded(!expanded);
    }

    return [
        <div id={props.id} key={props.id + "linktarget"}></div>,
            <Link key={props.id + 'link'} to={'/#' + props.id} style={{"textDecoration":"none", color:"black"}} onClick={toggleLines}>
                {expanded ? props.children : (
                    <TruncateMarkup
                        lines={props.lines}
                        ellipsis="..."
                    >
                        {props.children}
                    </TruncateMarkup>)}
                <p><em>Click anywhere to read more or less!</em></p>
            </Link>
    ];
};
