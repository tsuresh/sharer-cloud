import { useState, useEffect, useCallback, FormEvent, useRef } from 'react';
import type { ChangeEvent, MouseEvent } from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import {
  Box,
  Button,
  Card,
  Container,
  Divider,
  Grid,
  InputAdornment,
  Tab,
  Tabs,
  TextField,
  Typography
} from '@mui/material';
import { deviceApi } from '../../../__fake-api__/device-api';
import { AuthGuard } from '../../../components/authentication/auth-guard';
import { DashboardLayout } from '../../../components/dashboard/dashboard-layout';
import { DeviceListTable } from '../../../components/dashboard/device/device-list-table';
import { useMounted } from '../../../hooks/use-mounted';
import { Download as DownloadIcon } from '../../../icons/download';
import { Plus as PlusIcon } from '../../../icons/plus';
import { Search as SearchIcon } from '../../../icons/search';
import { Upload as UploadIcon } from '../../../icons/upload';
import { gtm } from '../../../lib/gtm';
import type { Device } from '../../../types/device';
import { Refresh } from '@mui/icons-material';

interface Filters {
  query?: string;
}

type TabValue = 'all';

interface Tab {
  label: string;
  value: TabValue;
}

const tabs: Tab[] = [
  {
    label: 'All',
    value: 'all'
  }
];

const applyFilters = (
  devices: Device[],
  filters: Filters
): Device[] => devices.filter((device) => {
  if (filters.query) {
    let queryMatched = false;
    const properties: ('name' | 'machineType')[] = ['name', 'machineType'];

    properties.forEach((property) => {
      if ((device[property]).toLowerCase().includes(filters.query!.toLowerCase())) {
        queryMatched = true;
      }
    });

    if (!queryMatched) {
      return false;
    }
  }

  return true;
});

const applyPagination = (
  devices: Device[],
  page: number,
  rowsPerPage: number
): Device[] => devices.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

const DeviceList: NextPage = () => {
  const isMounted = useMounted();
  const queryRef = useRef<HTMLInputElement | null>(null);
  const [devices, setDevices] = useState<Device[]>([]);
  const [currentTab, setCurrentTab] = useState<TabValue>('all');
  const [page, setPage] = useState<number>(0);
  const [rowsPerPage, setRowsPerPage] = useState<number>(10);
  const [filters, setFilters] = useState<Filters>({
    query: ''
  });

  useEffect(() => {
    gtm.push({ event: 'page_view' });
  }, []);

  const getDevices = useCallback(async () => {
    try {
      const data = await deviceApi.getDevices();

      if (isMounted()) {
        setDevices(data);
      }
    } catch (err) {
      console.error(err);
    }
  }, [isMounted]);

  useEffect(
    () => {
      getDevices();
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const handleQueryChange = (event: FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    setFilters((prevState) => ({
      ...prevState,
      query: queryRef.current?.value
    }));
  };

  const handlePageChange = (event: MouseEvent<HTMLButtonElement> | null, newPage: number): void => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (event: ChangeEvent<HTMLInputElement>): void => {
    setRowsPerPage(parseInt(event.target.value, 10));
  };

  // Usually query is done on backend with indexing solutions
  const filteredDevices = applyFilters(devices, filters);
  const paginatedDevices = applyPagination(filteredDevices, page, rowsPerPage);

  return (
    <>
      <Head>
        <title>
          Processing Network
        </title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8
        }}
      >
        <Container maxWidth="xl">
          <Box sx={{ mb: 4 }}>
            <Grid
              container
              justifyContent="space-between"
              spacing={3}
            >
              <Grid item>
                <Typography variant="h4">
                  Workload Network
                </Typography>
              </Grid>
              <Grid item>
                <Button
                  startIcon={<Refresh fontSize="small"/>}
                  onClick={getDevices}
                  variant="contained"
                >
                  Refresh
                </Button>
              </Grid>
            </Grid>
          </Box>
          <Card>
            <Tabs
              indicatorColor="primary"
              scrollButtons="auto"
              sx={{ px: 3 }}
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
            <Divider />
            <Box
              sx={{
                alignItems: 'center',
                display: 'flex',
                flexWrap: 'wrap',
                m: -1.5,
                p: 3
              }}
            >
              <Box
                component="form"
                onSubmit={handleQueryChange}
                sx={{
                  flexGrow: 1,
                  m: 1.5
                }}
              >
                <TextField
                  defaultValue=""
                  fullWidth
                  inputProps={{ ref: queryRef }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon fontSize="small" />
                      </InputAdornment>
                    )
                  }}
                  placeholder="Search devices"
                />
              </Box>

              {/*Sort removed from here*/}

            </Box>
            <DeviceListTable
              devices={paginatedDevices}
              devicesCount={filteredDevices.length}
              onPageChange={handlePageChange}
              onRowsPerPageChange={handleRowsPerPageChange}
              rowsPerPage={rowsPerPage}
              page={page}
            />
          </Card>
        </Container>
      </Box>
    </>
  );
};

DeviceList.getLayout = (page) => (
  <AuthGuard>
    <DashboardLayout>
      {page}
    </DashboardLayout>
  </AuthGuard>
);

export default DeviceList;
