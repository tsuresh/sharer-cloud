import { useState } from 'react';
import { Box, Button, Card, CardContent, CardHeader, Divider, TextField } from '@mui/material';

const states = [
    {
        value: 'DS-L1',
        label: 'Data Science L1'
    },
    {
        value: 'DS-L2',
        label: 'Data Science L2'
    },
    {
        value: 'GFX-L1',
        label: 'Video/Graphics Rendering L1'
    },
    {
        value: 'GFX-L2',
        label: 'Video/Graphics Rendering L2'
    }
];

export const RequestWorkload = (props) => {
    const [values, setValues] = useState({
        password: '',
        confirm: ''
    });

    const handleChange = (event) => {
        setValues({
            ...values,
            [event.target.name]: event.target.value
        });
    };

    return (
        <form {...props}>
            <Card>
                <CardHeader
                    subheader="Request Workload"
                    title="Workloads"
                />
                <Divider />
                <CardContent>
                    <TextField
                        fullWidth
                        label="Workload name"
                        margin="normal"
                        name="name"
                        onChange={handleChange}
                        type="text"
                        value={values.name}
                        variant="outlined"
                    />
                    <TextField
                        fullWidth
                        label="Machine Type"
                        margin="normal"
                        name="state"
                        onChange={handleChange}
                        required
                        select
                        SelectProps={{ native: true }}
                        value={values.state}
                        variant="outlined"
                    >
                        {states.map((option) => (
                            <option
                                key={option.value}
                                value={option.value}
                            >
                                {option.label}
                            </option>
                        ))}
                    </TextField>

                    <div style={{ 'padding-top': '15px' }}>Upload workload</div>

                    <TextField
                        fullWidth
                        margin="normal"
                        name="name"
                        onChange={handleChange}
                        type="file"
                        value={values.name}
                        variant="outlined"
                    />

                    <div style={{ 'padding-top': '15px' }}>Upload artefact</div>

                    <TextField
                        fullWidth
                        margin="normal"
                        name="name"
                        onChange={handleChange}
                        type="file"
                        value={values.name}
                        variant="outlined"
                    />

                </CardContent>
                <Divider />
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'flex-end',
                        p: 2
                    }}
                >
                    <Button
                        color="primary"
                        variant="contained"
                    >
                        Update
                    </Button>
                </Box>
            </Card>
        </form>
    );
};
