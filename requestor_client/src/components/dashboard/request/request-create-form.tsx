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

export const RequestCreateForm: FC = (props) => {
  const router = useRouter();
  const [files, setFiles] = useState<File[]>([]);
  const formik = useFormik({
    initialValues: {
      barcode: '925487986526',
      description: '',
      images: [],
      name: '',
      newPrice: 0,
      oldPrice: 0,
      sku: 'IYV-8745',
      submit: null,
      machineType: 'L1-DS',
      outputType: 'logs'
    },
    validationSchema: Yup.object({
      barcode: Yup.string().max(255),
      description: Yup.string().max(5000),
      images: Yup.array(),
      name: Yup.string().max(255).required(),
      newPrice: Yup.number().min(0).required(),
      oldPrice: Yup.number().min(0),
      sku: Yup.string().max(255)
    }),
    onSubmit: async (values, helpers): Promise<void> => {
      try {
        // NOTE: Make API request
        toast.success('Product created!');
        router.push('/dashboard/products').catch(console.error);
      } catch (err) {
        console.error(err);
        toast.error('Something went wrong!');
        helpers.setStatus({ success: false });
        helpers.setErrors({ submit: err.message });
        helpers.setSubmitting(false);
      }
    }
  });

  const handleDrop = (newFiles: File[]): void => {
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  const handleRemove = (file: File): void => {
    setFiles((prevFiles) => prevFiles.filter((_file) => _file.path !== file.path));
  };

  const handleRemoveAll = (): void => {
    setFiles([]);
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
                label="Product Name"
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
                files={files}
                onDrop={handleDrop}
                onRemove={handleRemove}
                onRemoveAll={handleRemoveAll}
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
                files={files}
                onDrop={handleDrop}
                onRemove={handleRemove}
                onRemoveAll={handleRemoveAll}
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
