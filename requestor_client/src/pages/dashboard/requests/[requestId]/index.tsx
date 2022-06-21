import { useCallback, useState, useEffect } from 'react';
import type { ChangeEvent } from 'react';
import type { NextPage } from 'next';
import NextLink from 'next/link';
import Head from 'next/head';
import {
  Avatar,
  Box,
  Button,
  Chip,
  Container,
  Divider,
  Grid,
  Link,
  Tab,
  Tabs,
  Typography
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { AuthGuard } from '../../../../components/authentication/auth-guard';
import { DashboardLayout } from '../../../../components/dashboard/dashboard-layout';
import { CustomerBasicDetails } from '../../../../components/dashboard/customer/customer-basic-details';
import { CustomerDataManagement } from '../../../../components/dashboard/customer/customer-data-management';
import { CustomerEmailsSummary } from '../../../../components/dashboard/customer/customer-emails-summary';
import { CustomerInvoices } from '../../../../components/dashboard/customer/customer-invoices';
import { CustomerPayment } from '../../../../components/dashboard/customer/customer-payment';
import { CustomerLogs } from '../../../../components/dashboard/customer/customer-logs';
import { useMounted } from '../../../../hooks/use-mounted';
import { ChevronDown as ChevronDownIcon } from '../../../../icons/chevron-down';
import { PencilAlt as PencilAltIcon } from '../../../../icons/pencil-alt';
import { gtm } from '../../../../lib/gtm';
import type { Customer } from '../../../../types/customer';
import { getInitials } from '../../../../utils/get-initials';
import { requestApi } from 'src/__fake-api__/request-api';
import { Request } from 'src/types/request';

const tabs = [
  { label: 'Details', value: 'details' },
  { label: 'Results', value: 'results' },
  { label: 'Console', value: 'console' }
];

const CustomerDetails: NextPage = () => {
  const isMounted = useMounted();

  const [request, setRequest] = useState<Request | null>(null);
  const [currentTab, setCurrentTab] = useState<string>('details');

  useEffect(() => {
    gtm.push({ event: 'page_view' });
  }, []);

  const getWorkload = useCallback(async (workload_id: string) => {
    try {

      console.log(workload_id);

      const data = await requestApi.getRequest(workload_id)

      if (isMounted()) {
        setRequest(data);
      }
    } catch (err) {
      console.error(err);
    }
  }, [isMounted]);

  useEffect(
    () => {
      const path = window.location.pathname.split("/");
      getWorkload(path[path.length-1]);
    },
    []
  );
  
  const handleTabsChange = (event: ChangeEvent<{}>, value: string): void => {
    setCurrentTab(value);
  };

  if (!request) {
    return null;
  }

  return (
    <>
      <Head>
        <title>
          Workload Detail
        </title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8
        }}
      >
        <Container maxWidth="md">
          <div>
            <Box sx={{ mb: 4 }}>
              <NextLink
                href="/dashboard/requests"
                passHref
              >
                <Link
                  color="textPrimary"
                  component="a"
                  sx={{
                    alignItems: 'center',
                    display: 'flex'
                  }}
                >
                  <ArrowBackIcon
                    fontSize="small"
                    sx={{ mr: 1 }}
                  />
                  <Typography variant="subtitle2">
                    Workloads
                  </Typography>
                </Link>
              </NextLink>
            </Box>
            <Grid
              container
              justifyContent="space-between"
              spacing={3}
            >
              <Grid
                item
                sx={{
                  alignItems: 'center',
                  display: 'flex',
                  overflow: 'hidden'
                }}
              >
                <div>
                  <Typography variant="h4">
                    {request.workload_name}
                  </Typography>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <Typography variant="subtitle2">
                      workload_id:
                    </Typography>
                    <Chip
                      label={request.workload_id}
                      size="small"
                      sx={{ ml: 1 }}
                    />
                  </Box>
                </div>
              </Grid>
              <Grid
                item
                sx={{ m: -1 }}
              >
                {/* <NextLink
                  href="/dashboard/customers/1/edit"
                  passHref
                >
                  <Button
                    component="a"
                    endIcon={(<PencilAltIcon fontSize="small" />)}
                    sx={{ m: 1 }}
                    variant="outlined"
                  >
                    Edit
                  </Button>
                </NextLink> */}
                <Button
                  endIcon={(<ChevronDownIcon fontSize="small" />)}
                  sx={{ m: 1 }}
                  variant="contained"
                >
                  Actions
                </Button>
              </Grid>
            </Grid>
            <Tabs
              indicatorColor="primary"
              onChange={handleTabsChange}
              scrollButtons="auto"
              sx={{ mt: 3 }}
              textColor="primary"
              value={currentTab}
              variant="scrollable"
            >
              {tabs.map((tab) => (
                <Tab
                  key={tab.value}
                  label={tab.label}
                  value={tab.value}
                />
              ))}
            </Tabs>
          </div>
          <Divider />
          <Box sx={{ mt: 3 }}>
            {currentTab === 'details' && (
              <Grid
                container
                spacing={3}
              >
                <Grid
                  item
                  xs={12}
                >
                  <CustomerBasicDetails
                    workload_name={request.workload_name}
                    user_id={request.user_id}
                    artefact_url={request.artefact_url}
                    spec_url={request.spec_url}
                    machine_type={request.machine_type}
                    machine_image={request.machine_image}
                    status={request.status}
                    replicas={request.replicas}
                  />
                </Grid>
                {/* <Grid
                  item
                  xs={12}
                >
                  <CustomerDataManagement />
                </Grid> */}
              </Grid>
            )}
            {currentTab === 'results' && <CustomerInvoices />}
            {currentTab === 'console' && <CustomerLogs />}
          </Box>
        </Container>
      </Box>
    </>
  );
};

CustomerDetails.getLayout = (page) => (
  <AuthGuard>
    <DashboardLayout>
      {page}
    </DashboardLayout>
  </AuthGuard>
);

export default CustomerDetails;

