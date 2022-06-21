import { useState } from 'react';
import type { FC } from 'react';
import { useRouter } from 'next/router';
import toast from 'react-hot-toast';
import * as Yup from 'yup';
import { useFormik } from 'formik';
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControlLabel,
  FormHelperText,
  Grid,
  MenuItem,
  Switch,
  TextField,
  Typography
} from '@mui/material';
import { FileDropzone } from '../../file-dropzone';
import type { File } from '../../file-dropzone';
import { QuillEditor } from '../../quill-editor';

const machineTypeOptions = [
  {
    label: 'Data Science L1',
    value: 'L1-DS'
  },
  {
    label: 'Data Science L2',
    value: 'L2-DS'
  },
  {
    label: 'Data Science L3',
    value: 'L3-DS'
  },
  {
    label: 'Rendering L1',
    value: 'L1-RD'
  },
  {
    label: 'Rendering L2',
    value: 'L2-RD'
  },
  {
    label: 'Rendering L3',
    value: 'L3-RD'
  }
];

const outputTypeOptions = [
  {
    label: 'Execution Logs',
    value: 'logs'
  },
  {
    label: 'Raw file',
    value: 'file'
  },
  {
    label: 'Network',
    value: 'network'
  },
];

const replicaOptions  = Array.from(Array(10).keys()).map(value => {
  return {
    label: `${value} replicas`,
    value: value,
  };
});

export const RequestCreateForm: FC = (props) => {
  const router = useRouter();

  const [configFiles, setConfigFiles] = useState<File[]>([]);
  const [artefactFiles, setArtefactFiles] = useState<File[]>([]);

  const [configFileUrl, setConfigFileUrl] = useState("");
  const [artefactFileUrl, setArtefactFileUrl] = useState("");

  const formik = useFormik({
    initialValues: {
      description: '',
      images: [],
      name: '',
      submit: null,
      machineType: 'L1-DS',
      outputType: 'logs',
      replicas: 1
    },
    validationSchema: Yup.object({
      description: Yup.string().max(5000),
      images: Yup.array(),
      name: Yup.string().max(255).required(),
      machineType: Yup.string().required(),
      outputType: Yup.string().required(),
      replicas: Yup.number().max(10).required(),
    }),
    onSubmit: async (values, helpers): Promise<void> => {
      try {
        if(configFileUrl == "" || artefactFileUrl == ""){
          toast.error('Please make sure to upload the files before proceeding!');
        } else {
          var myHeaders = new Headers();
          myHeaders.append("Content-Type", "application/json");

          var raw = JSON.stringify({
            "user_id": "123",
            "workload_name": values.name,
            "artefact_url": artefactFileUrl,
            "spec_url": configFileUrl,
            "machine_type": values.machineType,
            "output_type": values.outputType,
            "replicas" : values.replicas
          });

          var requestOptions: any = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
          };

          fetch("http://localhost:5000/requestWorkloadProcess", requestOptions)
            .then(response => response.text())
            .then(result => {
              toast.success('Workload requested!')
              router.push('/dashboard/requests').catch(console.error);
            })
            .catch(error => toast.error('An error has occured while requesting!'));
        }
      } catch (err) {
        console.error(err);
        toast.error('Something went wrong!');
        helpers.setStatus({ success: false });
        helpers.setErrors({ submit: err.message });
        helpers.setSubmitting(false);
      }
    }
  });

  const uploadArtefactFile = () => {
    if (artefactFiles.length) {
      const formData = new FormData();
      formData.append('file', artefactFiles[0]);
      formData.append('type', 'artefact');
      fetch(
        'http://localhost:5000/upload',
        {
          method: 'POST',
          body: formData,
        }
      )
        .then((response) => response.json())
        .then((result) => {
          console.log('Success:', result);
          setArtefactFileUrl(result["url"]);
          toast.success('File successfully uploaded');
        })
        .catch((error) => {
          console.error('Error:', error);
          toast.success('File failed uploading');
        });
    }
  }

  const uploadConfigFile = () => {
    if(configFiles.length > 0){
      const formData = new FormData();
      formData.append('file', configFiles[0]);
      formData.append('type', 'spec');
      fetch(
        'http://localhost:5000/upload',
        {
          method: 'POST',
          body: formData,
        }
      )
        .then((response) => response.json())
        .then((result) => {
          console.log('Success:', result);
          setConfigFileUrl(result["url"]);
          toast.success('File successfully uploaded');
        })
        .catch((error) => {
          console.error('Error:', error);
          toast.success('File failed uploading');
        });
    }
  }

  const handleDrop = (newFiles: File[]): void => {
    setConfigFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleRemove = (file: File): void => {
    setConfigFiles((prevFiles) => prevFiles.filter((_file) => _file.path !== file.path));
  };

  const handleRemoveAll = (): void => {
    setConfigFiles([]);
  };

  const handleArtefactDrop = (newFiles: File[]): void => {
    setArtefactFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleArtefactRemove = (file: File): void => {
    setArtefactFiles((prevFiles) => prevFiles.filter((_file) => _file.path !== file.path));
  };

  const handleArtefactRemoveAll = (): void => {
    setArtefactFiles([]);
  };

  return (
    <form
      onSubmit={formik.handleSubmit}
      {...props}
    >
      <Card>
        <CardContent>
          <Grid
            container
            spacing={3}
          >
            <Grid
              item
              md={4}
              xs={12}
            >
              <Typography variant="h6">
                Basic details
              </Typography>
            </Grid>
            <Grid
              item
              md={8}
              xs={12}
            >
               <Typography
                color="textSecondary"
                sx={{
                  mb: 2
                }}
                variant="subtitle2"
              >
                Workload Name
              </Typography>
              <TextField
                error={Boolean(formik.touched.name && formik.errors.name)}
                fullWidth
                helperText={formik.touched.name && formik.errors.name}
                label="Workload Name"
                name="name"
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                value={formik.values.name}
              />
              <Typography
                color="textSecondary"
                sx={{
                  mb: 2,
                  mt: 3
                }}
                variant="subtitle2"
              >
                Workload Type
              </Typography>
              <TextField
                error={Boolean(formik.touched.machineType && formik.errors.machineType)}
                fullWidth
                label="Workload Type"
                name="machineType"
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                select
                value={formik.values.machineType}
              >
                {machineTypeOptions.map((option) => (
                  <MenuItem
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>

              <Typography
                color="textSecondary"
                sx={{
                  mb: 2,
                  mt: 3
                }}
                variant="subtitle2"
              >
                Output Type
              </Typography>

              <TextField
                error={Boolean(formik.touched.outputType && formik.errors.outputType)}
                fullWidth
                label="Output Type"
                name="outputType"
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                select
                value={formik.values.outputType}
              >
                {outputTypeOptions.map((option) => (
                  <MenuItem
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>

              <Typography
                color="textSecondary"
                sx={{
                  mb: 2,
                  mt: 3
                }}
                variant="subtitle2"
              >
                Replica Count
              </Typography>

              <TextField
                error={Boolean(formik.touched.replicas && formik.errors.replicas)}
                fullWidth
                label="Replicas"
                name="replicas"
                onBlur={formik.handleBlur}
                onChange={formik.handleChange}
                select
                value={formik.values.replicas}
              >
                {replicaOptions.map((option) => (
                  <MenuItem
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>


              {Boolean(formik.touched.description && formik.errors.description) && (
                <Box sx={{ mt: 2 }}>
                  <FormHelperText error>
                    {formik.errors.description}
                  </FormHelperText>
                </Box>
              )}
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Grid
            container
            spacing={3}
          >
            <Grid
              item
              md={4}
              xs={12}
            >
              <Typography variant="h6">
                Configuration
              </Typography>
              <Typography
                color="textSecondary"
                variant="body2"
                sx={{ mt: 1 }}
              >
                Please upload the YAML file consisting the configuration
              </Typography>
            </Grid>
            <Grid
              item
              md={8}
              xs={12}
            >
              <FileDropzone
                accept=".yaml"
                files={configFiles}
                onDrop={handleDrop}
                onRemove={handleRemove}
                onRemoveAll={handleRemoveAll}
                onUpload={uploadConfigFile}
                maxFiles={1}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Grid
            container
            spacing={3}
          >
            <Grid
              item
              md={4}
              xs={12}
            >
              <Typography variant="h6">
                Artefact
              </Typography>
              <Typography
                color="textSecondary"
                variant="body2"
                sx={{ mt: 1 }}
              >
                Please upload the code/data artefacts in ZIP format
              </Typography>
            </Grid>
            <Grid
              item
              md={8}
              xs={12}
            >
              <FileDropzone
                accept=".zip"
                files={artefactFiles}
                onDrop={handleArtefactDrop}
                onRemove={handleArtefactRemove}
                onRemoveAll={handleArtefactRemoveAll}
                onUpload={uploadArtefactFile}
                maxFiles={1}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
          mx: -1,
          mb: -1,
          mt: 3
        }}
      >

        <Button
          sx={{ m: 1, ml: 'auto' }}
          variant="outlined"
        >
          Cancel
        </Button>
        <Button
          sx={{ m: 1 }}
          type="submit"
          variant="contained"
        >
          Create
        </Button>
      </Box>
    </form>
  );
};
