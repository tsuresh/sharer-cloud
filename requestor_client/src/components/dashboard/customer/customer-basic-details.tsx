import type { FC } from 'react';
import PropTypes from 'prop-types';
import { Button, Card, CardActions, CardHeader, Divider, useMediaQuery } from '@mui/material';
import type { Theme } from '@mui/material';
import { PropertyList } from '../../property-list';
import { PropertyListItem } from '../../property-list-item';

interface CustomerBasicDetailsProps {
  workload_name?: string;
  user_id?: string;
  artefact_url?: string;
  spec_url?: string;
  machine_type?: string;
  machine_image?: string;
  status?: string;
  replicas?: string;
}


export const CustomerBasicDetails: FC<CustomerBasicDetailsProps> = (props) => {
  const { workload_name, user_id, artefact_url, spec_url, machine_type, machine_image, status, replicas, ...other } = props;
  const mdUp = useMediaQuery((theme: Theme) => theme.breakpoints.up('md'));

  const align = mdUp ? 'horizontal' : 'vertical';

  //Download artefact
  const downloadArtefact = () => {
    window.location.href = `${artefact_url}`; 
  }
  
  //Download spec 
  const downloadSpec = () => {
    window.location.href = `${spec_url}`; 
  }

  return (
    <Card {...other}>
      <CardHeader title="Basic Details" />
      <Divider />
      <PropertyList>
        <PropertyListItem
          align={align}
          divider
          label="Workload Name"
          value={workload_name}
        />
        <PropertyListItem
          align={align}
          divider
          label="Artefact URL"
          value={artefact_url}
        />
        <PropertyListItem
          align={align}
          divider
          label="Spec URL"
          value={spec_url}
        />
        <PropertyListItem
          align={align}
          divider
          label="Machine Type"
          value={machine_type}
        />
        <PropertyListItem
          align={align}
          divider
          label="Machine Image"
          value={machine_image}
        />
        <PropertyListItem
          align={align}
          divider
          label="Status"
          value={status}
        />
        <PropertyListItem
          align={align}
          divider
          label="Number of Replicas"
          value={replicas}
        />
      </PropertyList>
      <CardActions
        sx={{
          flexWrap: 'wrap',
          px: 3,
          py: 2,
          m: -1
        }}
      >
        <Button
          sx={{ m: 1 }}
          variant="outlined"
          onClick={downloadArtefact}
        >
          Download Artefact
        </Button>
       
        <Button
          sx={{ m: 1 }}
          variant="outlined"
          onClick={downloadSpec}
        >
          Download Spec
        </Button>

      </CardActions>
    </Card>
  );
};

CustomerBasicDetails.propTypes = {
  workload_name: PropTypes.string,
  user_id: PropTypes.string,
  artefact_url: PropTypes.string,
  spec_url: PropTypes.string,
  machine_type: PropTypes.string,
  machine_image: PropTypes.string,
  status: PropTypes.string,
  replicas: PropTypes.string,
};
