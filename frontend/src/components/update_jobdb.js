import React, { useState } from "react";
import { useNavigate } from "react-router";
    
export default function UpdateDB() {
    const navigate = useNavigate();
    
    // This function will handle the click
    async function onClick(e) {
        e.preventDefault();

        console.log("[FRONTEND] Updating jobdb...");
        await fetch("http://localhost:5050/update_jobdb_exec/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({"update_jobdb":null}),
        })
        .catch(error => {
            window.alert(error);
            return;
        });
    
        navigate("/");
    }
    
    return (
        <div>
            <h3>Update Database</h3>
            <button
                onClick = {onClick}
                type="submit"
                value="Update database"
                className="btn btn-primary"
            />
        </div>
    );
}
